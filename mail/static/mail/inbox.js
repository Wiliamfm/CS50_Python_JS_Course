document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(replyRecipient, replySubject, replyBody, replyTimestamp) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none'
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if(replyRecipient==undefined || replySubject==undefined || replyBody==undefined || replyTimestamp==undefined){
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value ='' ;
    document.querySelector('#compose-body').value ='' ;
  }else{
    document.querySelector('#compose-recipients').value = replyRecipient;
    let re = /^(Re:)/;
    if(re.test(replySubject)){
      document.querySelector('#compose-subject').value = replySubject;
    }else{
      document.querySelector('#compose-subject').value = 'Re: ' +replySubject;
    }

    document.querySelector('#compose-body').value = `On ${replyTimestamp} ${replyRecipient} wrote:\n ${replyBody}\n`;
  }

  document.forms['compose-form'].onsubmit = function() {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value,
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        if(result.message != undefined){
          load_mailbox('sent');
        }else{
          const d= document.createElement('div');
          d.className= 'alert alert-danger';
          d.tabIndex= -1;
          d.innerHTML= result.error;
          const c= document.querySelector('#compose-view');
          c.insertBefore(d, c.firstChild);
          d.focus();
        }
    });
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    const div= document.createElement('div');
    div.className = 'container';
    const table= document.createElement('table');
    table.className= 'table';
    const tableBody= document.createElement('tbody');
    table.appendChild(tableBody);
    div.appendChild(table);
    emails.forEach(email => {
      const tr = document.createElement('tr');
      tr.style= 'background-color: white;';
      const tdSender = document.createElement('td');
      tdSender.textContent= email.sender;
      tr.appendChild(tdSender);
      const tdSubject = document.createElement('td');
      if(email.subject){
        tdSubject.textContent= email.subject;
      }else{
        tdSubject.textContent= 'No subject';
      }
      tr.appendChild(tdSubject);
      const tdId= document.createElement('td');
      tdId.textContent= email.id;
      tdId.style= 'display: None';
      tr.appendChild(tdId);
      const tdTime = document.createElement('td');
      tdTime.textContent= email.timestamp;
      tr.appendChild(tdTime);
      if(mailbox!='sent'){
        let btn= document.createElement('button');
        if(email.archived){
          btn.textContent= 'unarchive';
        }else{
          btn.textContent= 'archive';
        }
        btn.addEventListener('click', function(){btnArchive(email.id, email.archived)}, false);
        tr.appendChild(btn);
      }
      tr.onclick= loadEmailView;
      tr.onmouseover= trOnMouse;
      tr.onmouseout= trOnMouseOut;
      //console.log(email);
      if(email.read){
        tr.style= 'background-color: gray;';
      }
      tableBody.appendChild(tr);
    })
    document.querySelector('#emails-view').appendChild(div);
  });
}

function btnArchive(id, arc){
  let a = arc ? false : true;
  console.log(id,arc, 'fuck this btn');
  fetch(`/emails/${id}`,{
    method: 'PUT', 
    body: JSON.stringify({
      archived: a
    })
  });
}

function  loadEmailView(){
  //Show corresponging div
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  //load the email´s details
  fetch(`emails/${this.children[2].innerText}`)
  .then(response => response.json())
  .then(email => {
    const div= document.querySelector('#email-view');
    const sender= document.querySelector('#sender');
    sender.textContent= 'By: ' + email.sender;
    sender.style.fontStyle= 'bold';
    const recipients= document.querySelector('#recipients');
    let r= '';
    for(var i=0; i<email.recipients.length; i++) {
      r += email.recipients[i] + ' ';
    }
    recipients.textContent= 'to: ' +r;
    const subject= document.querySelector('#subject');
    subject.textContent= 'Subject: ' +email.subject;
    const timestamp= document.querySelector('#timestamp');
    timestamp.textContent= email.timestamp;
    timestamp.style= 'text-align: right; font-style: italic;';
    const body= document.querySelector('#body');
    body.textContent= email.body;
    const btn= document.querySelector('#btn');
    btn.addEventListener('click', () => {
      compose_email(email.sender, email.subject, email.body, email.timestamp);
    });
    fetch('/emails/'+email.id,{
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });
    //console.log(email)
  });
}

function trOnMouse(){
  document.body.style.cursor= 'pointer';
}

function trOnMouseOut(){
  document.body.style.cursor= 'default';
}