var canLike= true;
document.addEventListener('DOMContentLoaded', function(){
  loadTable(1);
  try{
    document.querySelector('#btnFollow').addEventListener('click', btnFollow);
  }catch (e){
    console.log("Not valid follow");
  }
});

function loadTable(numberPage){
  let div= document.querySelector("#listPosts");
  div.innerHTML="";
  fetch('/user/' +username +"/" +numberPage)
  .then(response => response.json())
  .then(data => {
    data['posts'].forEach(post => {
      let divContainer= document.createElement("div");
      divContainer.className= "list-group-item container d-flex flex-column";
      let a= document.createElement("a");
      a.className= "list-group-item-action";
      let divUser= document.createElement("div");
      divUser.className= "d-flex flex-row mb-2 align-items-center justify-content-between";
      let divContent= document.createElement("div");
      divContent.className= "list-group-item d-flex flex-row align-items-center justify-content-between";
      let divLikes= document.createElement("div");
      divLikes.className= "d-flex flex-row align-items-center justify-content-between";
      divLikes.style.margin= "10px";
      let h3= document.createElement("h3");
      h3.className= "p-2";
      h3.innerText= post.user;
      let small= document.createElement("small");
      small.innerText= post.date;
      divUser.appendChild(h3);
      divUser.appendChild(small);
      a.appendChild(divUser);
      a.href= urlProfile.replace('user_id', post.user);
      divContainer.appendChild(a);
      let p= document.createElement("p");
      p.innerText= post.text;
      divContent.appendChild(p);
      divContainer.appendChild(divContent);
      let h5= document.createElement("h5");
      h5.innerText= 'Likes: ' + post.likes;
      let postId= document.createElement('p');
      postId.textContent= post.id;
      postId.hidden= true;
      let btnLikes= document.createElement("button");
      if(!netUser == ""){
        btnLikes.className= "btn btn-primary";
      }else{
        btnLikes.className= "btn btn-primary disabled";
        btnLikes.disabled= true;
      }
      if(post.userLike.includes(netUser)){
        btnLikes.textContent= "Unlike";
      }else{
        btnLikes.textContent= "Like";
      }
      btnLikes.onclick= () => {
        let cLike= true;
        if(btnLikes.textContent === "Like"){
          addLike(post.id, true)
        }else{
          addLike(post.id, false)
        }
      }
      divLikes.appendChild(postId);
      divLikes.appendChild(h5);
      //divLikes.appendChild(btnLikes);
      if(canEdit){
        let btnEdit= document.createElement("button");
        btnEdit.className= "btn btn-primary";
        btnEdit.textContent= "Edit";
        btnEdit.onclick= () => {
          editPost(divContent, p, btnEdit, postId);
        };
        divLikes.append(btnEdit);
      }
      divContainer.appendChild(divLikes);
      div.appendChild(divContainer);
    })
    let divPagination = document.querySelector('#divPagination');
    let previous= document.querySelector('#liPrevious');
    let next= document.querySelector('#liNext')
    let current= document.querySelector('#liCurrentPage');
    current.innerHTML= `
      <span class="page-link">
          ` +data.number +`
          <span class="sr-only">(current)</span>
      </span>
    `;
    console.log(data);
    if(data.previousPageNumber != -1){
      previous.className= "page-item";
      previous.innerHTML= `
        <a class="page-link" id="linkPreviousPage" href="#">Previous</a>
      `;
      let a= document.querySelector('#linkPreviousPage');
      a.addEventListener('click', () => {
        loadTable(data.previousPageNumber);
      });
    }else{
      previous.className= "page-item disabled";
      previous.innerHTML= `
        <span class="page-link">Previous</span>
      `;
    }
    if(data.nextPageNumber != -1){
      next.className= "page-item";
      next.innerHTML= `
        <a class="page-link" id="linkNextPage" href="#">Next</a>
      `;
      let a= document.querySelector('#linkNextPage');
      a.addEventListener('click', () => {
        loadTable(data.nextPageNumber);
      });
    }else{
      next.className= "page-item disabled";
      next.innerHTML= `
        <span class="page-link">next</span>
      `;
    }
  });
}

function btnFollow(){
  console.log("follow");
  fetch('/user/' +username ,{
    method: 'PUT',
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)
    window.location.reload();
  });
}

function editPost(divContent, postText, btnEdit, postId){
  divContent.innerHTML= "";
  let textArea= document.createElement("textarea");
  textArea.value= postText.textContent;
  textArea.style.width= "100%";
  divContent.appendChild(textArea);
  btnEdit.textContent= "Save";
  btnEdit.onclick= () => {
    data= {
      text: textArea.value,
      id: postId.textContent
    }
    fetch('post', {
      method: 'PUT',
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if(data.message === "success"){
        loadTable(1);
      }
    });
    btnEdit.textContent="Edit";
  }
}

function addLike(postId, canLike){
  if(canLike){
    fetch("post/like/"+postId)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      loadTable(1);
    })
  }else{
    fetch("post/like/"+postId, {
      method: "PUT",
      body: JSON.stringify({canLike: false})
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      loadTable(1);
    })
  }
}