// adapted from https://www.twilio.com/blog/fax-email-sendgrid-nodejs
// Must have SENDGRID_API_KEY, SENDER_NAME, FROM_EMAIL_ADDRESS, and TO_EMAIL_ADDRESS env vars configured in Runtime -> Functions -> Configure for this to work
const request = require('request');

exports.handler = function (context, event, callback) {
  if (event.Fax === "failed")
    return callback("Fax itself failed, so nothing to do.  Goodbye!");

  request.get({ uri: event.MediaUrl, encoding: null }, (error, response, body) => {
    if (error || response.statusCode !== 200)
      return callback("Failed to retrieve fax from twilio's servers.  Was one not recieved?");

    const email = {
      personalizations: [{ to: [{ email: context.TO_EMAIL_ADDRESS }] }],
      from: { email: context.FROM_EMAIL_ADDRESS, name: context.SENDER_NAME },
      reply_to: { email: context.FROM_EMAIL_ADDRESS, name: context.SENDER_NAME },
      subject: `Got fax from ${event.From}`,
      content: [{
        type: 'text/plain',
        value: `Fax was received at ${new Date()} and is attached to this email.`
      }],
      attachments: [{
        content: body.toString('base64'),
        filename: `${event.FaxSid}.pdf`,
        type: response.headers['content-type']
      }]
    };

    request.post({
        uri: 'https://api.sendgrid.com/v3/mail/send',
        body: email,
        auth: {bearer: context.SENDGRID_API_KEY},
        json: true
      },
      (error, response, body) => {
        if (error)
          return callback(JSON.stringify(error));
        else if (response.statusCode === 202) // worked, send an empty twiml response
          return callback(null, new Twilio.twiml.VoiceResponse());
        else // something went wrong
          return callback(JSON.stringify(body));
      }
    );
  });
}