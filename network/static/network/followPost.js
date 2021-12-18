document.addEventListener('DOMContentLoaded', function(){
  loadTable(1);
});

function loadTable(pageNumber){
  let div= document.querySelector("#listPosts");
  div.innerHTML= "";
  fetch('/post/getFollowsPosts/' +pageNumber)
  .then(response => response.json())
  .then(data => {
    data["posts"].forEach(post => {
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
      let h3= document.createElement("h3");
      h3.className= "p-2";
      h3.innerText= post.user;
      let small= document.createElement("small");
      small.innerText= post.date;
      divUser.appendChild(h3);
      divUser.appendChild(small);
      a.appendChild(divUser);
      //console.log(urlProfile);
      a.href= urlProfile.replace('user_id', post.user);
      divContainer.appendChild(a);
      let p= document.createElement("p");
      p.innerText= post.text;
      divContent.appendChild(p);
      divContainer.appendChild(divContent);
      let h5= document.createElement("h5");
      h5.innerText= 'Likes: ' + post.likes;
      divLikes.appendChild(h5);
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
