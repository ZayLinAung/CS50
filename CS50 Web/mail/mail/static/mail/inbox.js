document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');

    let recipients = document.querySelector('#compose-recipients');
    let subject = document.querySelector('#compose-subject');
    let body = document.querySelector('#compose-body');

    document.querySelector('#compose-form').onsubmit = ()=> {
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients.value,
            subject: subject.value,
            body: body.value
        })
      })
      .then(response => response.json())
      .then(result => {
          load_mailbox('sent');
          let noti = document.querySelector('#noti-view')
          noti.style.display = 'block';
          if("message" in result){
            noti.className = "alert alert-success";
            noti.innerHTML = result.message;
          }
          else{
            noti.className = "alert alert-danger";
            noti.innerHTML = result.error;
          }
      });
      return false;
    }
  });

  function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#noti-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#container').innerHTML = '';
    document.querySelector('#mailView').innerHTML = '';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
    document.querySelector('#container').innerHTML = '';
  }

  function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#noti-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#container').innerHTML = '';
    document.querySelector('#mailView').innerHTML = '';

    // Show the mailbox name
    let emailView = document.querySelector('#emails-view')
    emailView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Print emails
        for(index in emails){
          const element = document.createElement('div');
          element.style.width = "auto";
          element.style.height = "30px";
          let id = emails[index]["id"]
          element.innerHTML = `
          <button style = "background: #B2B2B2;" class='orders-render' data-id = ${emails[index]["id"]} id = ${id} onclick="viewMail(${id}, ${mailbox == 'sent'})">
          <span> ${emails[index]["sender"]} </span>
          <span> ${emails[index]["subject"]} </span>
          <span> ${emails[index]["timestamp"]}</span>
          </button>`
          element.addEventListener('click', function() {
            console.log('This element has been clicked!')
        });

          document.querySelector('#container').append(element);
          if(emails[index]["read"] === true){
            document.getElementById(id).style.background = "white";
          }
        }
    });
  }

  function viewMail(id, boolean){
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read : true
      })
    })

    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#noti-view').style.display = 'none';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#container').innerHTML = '';
      document.querySelector('#mailView').innerHTML = `
      <h4>Subject: ${email["subject"]}</h4>
      <h6>Sender: ${email["sender"]}</h6>
      <h6>Recipients: ${email["recipients"]}</h6><br>
      ${email["timestamp"]}
      <hr>
      ${email["body"]} <br><br><hr>
      `;
      if (!boolean){
      const element = document.createElement('button');
      element.style.margin = "5px";
      if (email["archived"]){
        element.innerHTML = 'Unarchive';
      }
      else{
        element.innerHTML = 'Archive';
      }
      document.querySelector('#mailView').append(element);

      element.addEventListener('click', function() {
        if (element.innerHTML == 'Archive'){
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: true
            })
          })
        }
        else{
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: false
            })
          })
        }
        load_mailbox('inbox');
      });
    }
    const reply = document.createElement('button');
    reply.style.margin = "5px";
    reply.innerHTML = 'Reply';
    reply.addEventListener('click', function() {
        // Show compose view and hide other views
      document.querySelector('#noti-view').style.display = 'none';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      document.querySelector('#container').innerHTML = '';
      document.querySelector('#mailView').innerHTML = '';

      // Clear out composition fields
      document.querySelector('#compose-recipients').value = `${email["sender"]}`;
      document.querySelector('#compose-subject').value = `Re: ${email["subject"]}`;
      if(email["subject"].substring(0,3) === 'Re:')
        document.querySelector('#compose-subject').value = `${email["subject"]}`;
      document.querySelector('#compose-body').value = `On ${email["timestamp"]} ${email["sender"]} wrote:\n${email["body"]}`;
      document.querySelector('#container').innerHTML = '';
    });
    document.querySelector('#mailView').append(reply);
    });
  }
