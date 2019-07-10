// adapted from https://www.twilio.com/blog/fax-email-sendgrid-nodejs
// Must have SENDGRID_API_KEY, SENDER_NAME, FROM_EMAIL_ADDRESS, and TO_EMAIL_ADDRESS env vars configured in Runtime -> Functions -> Configure for this to work
const request = require('request');

exports.handler = function (context, event, callback) {
  const faxUrl = event.MediaUrl;

  request.get({ uri: faxUrl, encoding: null }, (error, response, body) => {
    const email = {
      personalizations: [
        { to: [{ email: context.TO_EMAIL_ADDRESS }] }
      ],
      from: { email: context.FROM_EMAIL_ADDRESS, name: context.SENDER_NAME },
      reply_to: { email: context.FROM_EMAIL_ADDRESS, name: context.SENDER_NAME },
      subject: `Got fax from ${event.From}`,
      content: [
        {
          type: 'text/html',
          value: `Fax was received at ${new Date()} and is attached to this email.`
        }
      ],
      attachments: []
    };
    if (!error && response.statusCode === 200) {
      email.attachments.push({
        content: body.toString('base64'),
        filename: `${event.FaxSid}.pdf`,
        type: response.headers['content-type']
      });
    }
    request.post(
      {
        uri: 'https://api.sendgrid.com/v3/mail/send',
        body: email,
        auth: {
          bearer: context.SENDGRID_API_KEY
        },
        json: true
      },
      (error, response, body) => {
        if (error) {
          return callback(JSON.stringify(error));
        } else {
          if (response.statusCode === 202) {
            return callback(null, new Twilio.twiml.VoiceResponse());
          } else {
            return callback(JSON.stringify(body));
          }
        }
      }
    );
  });
}