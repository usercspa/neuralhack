const sgMail = require('@sendgrid/mail');
const MessagingResponse = require('twilio').twiml.MessagingResponse;
module.exports = (req, res) => {
    //Specify API Key for Sendgrid
    sgMail.setApiKey(process.env.SENDGRID_API_KEY);

    //Set from address as <number>@EMAIL_DOMAIN
    const fromAddress = req.body.From.replace("+", "") + `@${process.env.EMAIL_DOMAIN}`;

    //Create Email
    const email = {
        to: process.env.TO_EMAIL_ADDRESS,
        from: fromAddress,
        subject: `New SMS message from: ${req.body.From}`,
        text: req.body.Body,
    };
    
    // Send the email
    sgMail.send(email)
        .then(response => {
            res.status(200).send(response); //Make sure we return correctly.
        })
};


const util = require('util');
const multer = require('multer');
const addrs = require("email-addresses");
const sgMail = require('@sendgrid/mail');
const twilio = require('twilio');

module.exports = async (req, res) => { 
    const client = twilio(process.env.TWILIO_ACCOUNT_SID,process.env.TWILIO_AUTH_TOKEN);
    await util.promisify(multer().any())(req, res);

    const from = req.body.from;
    const to = req.body.to;
    const subject = req.body.subject;
    const body = req.body.text;

    //Using email-addresses library to extract email details.
    const toAddress = addrs.parseOneAddress(to);
    const toName = toAddress.local;
    const fromAddress = addrs.parseOneAddress(from);
    const fromName = fromAddress.local;

    //Sending SMS with Twilio Client
    client.messages.create({
        to: `+${toName}`,
        from: process.env.TWILIO_PHONE_NUMBER,
        body: `Message from:${fromName}\n${body}`
    }).then(msg => {
        console.log(msg)
        res.status(200).send(msg.sid);
    }).catch(err => {
        //If we get an error when sending the SMS email the error message back to the sender
        sgMail.setApiKey(process.env.SENDGRID_API_KEY);

        // Create Email
        const email = {
            to: fromAddress.address,
            from: toAddress.address,
            subject: `Error Sending SMS to ${toAddress.local}`,
            text: `${err}\n For email from ${fromAddress.address}`,
        };
        //Send Email
        sgResp = sgMail.send(email)
            .then(response => {
                res.status(200).send("Sent Error Email");
            })
            .catch(error => {
                res.status(500);
            });
    });
};
