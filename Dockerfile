FROM python:alpine
ENV PYTHONUNBUFFERED 1

# EXPOSE 8000

WORKDIR /faxmachine
COPY requirements.txt /faxmachine/
RUN pip install --no-cache-dir -r requirements.txt
COPY faxmachine-project/ /faxmachine/
# RUN ls -al &&  pwd

# CMD ["gunicorn", "-b", "0.0.0.0:8000", "faxmachine.wgsi"]