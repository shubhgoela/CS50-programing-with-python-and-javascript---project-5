function newPost(){
    console.log("Function 'NewPost' initiated")
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        "/newpost",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        body: JSON.stringify({
            NewPostData: document.querySelector('#NewPostData').value,
        })
    })
    .then((response) => response.json())
    .then(result => {
        // Print result
        console.log(result);
        console.log(Object.keys(result))
        console.log(Object.keys(result) == "error")
        if (Object.keys(result) == "message"){
          console.log("Post data added")
          location.reload()
        }
        else{
          document.querySelector("#postError").innerHTML= result.error ;
          return false;
          }
    }).catch(error => {
          console.log(error)
          return false;
    });
  }

  function newComment(num){
    console.log("Function 'NewComment' initiated")
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        "/newcomment",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        body: JSON.stringify({
            post: num,
            NewCommentData: document.querySelector(`#NewCommentData-${num}`).value
        })
    })
    .then((response) => response.json())
    .then(result => {
        // Print result
        console.log(result);
        console.log(Object.keys(result))
        console.log(Object.keys(result) == "error")
        if (Object.keys(result) == "message"){
          console.log("Comment data added")
          location.reload()
        }
        else{
          document.querySelector(`#commentError-${num}`).innerHTML= result.error ;
          return false;
          }
    }).catch(error => {
          console.log(error)
          return false;
    });
  }

  function newRelation(item){
    const profile = document.querySelector('#profileName').value
    const value = item.value
    const f = parseInt(document.querySelector('#numfollowers').innerHTML)
    console.log(value)
    console.log(profile)  
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        "/newrelation",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        body: JSON.stringify({
            profile: profile,
            NewRelationData: value
        })
    })
    .then((response) => response.json())
    .then(result => {
        // Print result
        console.log(result);
        console.log(Object.keys(result))
        console.log(Object.keys(result) == "error")
        if (Object.keys(result) == "message"){
            if (value == "follow"){
                item.value = "unfollow"
                item.innerHTML = "Unfollow"
                document.querySelector('#numfollowers').innerHTML = f+1
            }else{
                item.value = "follow"
                item.innerHTML = "Follow"
                document.querySelector('#numfollowers').innerHTML = f-1
            }
            console.log(`message received : ${result.message}`)
        }
        else{
            console.log("No message received")
          return false;
          }
    }).catch(error => {
          console.log(error)
          return false;
    });
  }

  function updatePost_1(b_id){
    var button = document.querySelector(`#${b_id}`)
    const id = button.value
    const text = document.querySelector(`#card-text-${id}`).innerHTML
    if (!localStorage.getItem(`initial-post-${id}`)){
        localStorage.setItem(`initial-post-${id}`, text)
    }else{
        localStorage.setItem(`initial-post-${id}`, text)
    }
    console.log(`updatepost1-${id}`)
    console.log(`text : ${text}`)
    //var html = document.querySelector(`#card-body-${id}`).innerHTML
    var button = document.querySelector(`#button-${id}`)
    document.querySelector(`#card-body-${id}`)
    .innerHTML = `<textarea type="text" class="form-control mr-5" id="UpdatePostData-${id}" name="UpdatePostData-${id}">${text}</textarea>`
    button.innerHTML = "Save"
    button.setAttribute("onclick",`updatePost(this.id)`)
  }

  function updatePost(b_id){
    var button = document.querySelector(`#${b_id}`)
    const post_id = button.value
    //var error = document.querySelector(`#postError-${post_id}`)
    const text = document.querySelector(`#UpdatePostData-${post_id}`).value
    console.log(`updatePost-${post_id}`)
    console.log(`text : ${text}`)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        "/updatepost",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        body: JSON.stringify({
            id: post_id,
            PostData: text
        })
    })
    .then((response) => response.json())
    .then(result => {
        // Print result
        console.log(result);
        console.log(Object.keys(result))
        console.log(Object.keys(result) == "error")
        if (Object.keys(result) == "message"){
            document.querySelector(`#card-body-${post_id}`).innerHTML = `<p class="card-text" id="card-text-${post_id}">${text}</p>`
            button.innerHTML = "Edit"
            button.setAttribute("onclick","updatePost_1(this.id)")
            console.log(`message received : ${result.message}`)
        }
        else{
            if(localStorage.getItem(`initial-post-${post_id}`) != null){
                console.log("local storage found")
                console.log(result.error)
                var text_initial = localStorage.getItem(`initial-post-${post_id}`)
                console.log(`text_initial : ${text_initial}`)
                if(result.error == "Post not found"){
                     var error_text = "Post could not be updated at the moment. Please try again after sometime."
                    document.querySelector(`#card-body-${post_id}`).innerHTML = `<p class="card-text" id="card-text-${post_id}">${text_initial}</p><div><small id="postError-{{key}}" class="text-danger">${error_text}</small></div>`
                }else if(result.error == "Post blank"){
                    console.log("inide post blank error")
                    var error_text = "Post cannot be blank, try deleting instead."
                    document.querySelector(`#card-body-${post_id}`).innerHTML = `<p class="card-text" id="card-text-${post_id}">${text_initial}</p><div><small id="postError-{{key}}" class="text-danger">${error_text}</small></div>`
                }else{
                    var error_text = "You are not authorised to edit this post."   
                    document.querySelector(`#card-body-${post_id}`).innerHTML = `<p class="card-text" id="card-text-${post_id}">${text_initial}</p><div><small id="postError-{{key}}" class="text-danger">${error_text}</small></div>`
                }
                button.innerHTML = "Edit"
                button.setAttribute("onclick","updatePost_1(this.id)")
                return false;
            }
            else{
                document.querySelector(`#card-body-${post_id}`).innerHTML = `<p class="card-text" id="card-text-${post_id}">${text}</p>`
                if(result.error == "Post not found"){
                    error.innerHTML = "Post could not be updated at the moment. Please try again after sometime."
                }else if(result.error == "Post blank"){
                    error.innerHTML = "Post cannot be blank, try deleting instead."
                }else{
                    error.innerHTML = "You are not authorised to edit this post."   
                }
                button.innerHTML = "Edit"
                button.setAttribute("onclick","updatePost_1(this.id)")
                return false;
            }
        }
    }).catch(error => {
          console.log(`error : ${error}`)
          return false;
    });
  }

function deletePost(b_id){
    var button = document.querySelector(`#${b_id}`)
    const id = button.value
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        "/deletepost",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        body: JSON.stringify({
            id: id,
        })
    })
    .then((response) => response.json())
    .then(result => {
        // Print result
        console.log(result);
        console.log(Object.keys(result))
        console.log(Object.keys(result) == "error")
        if (Object.keys(result) == "message"){  
            console.log(`card-body-${id}`)
            const child = document.querySelector(`#card-body-${id}`)  
            child.parentElement.remove();   
            console.log(`message received : ${result.message}`)
            location.reload()
        }
        else{
            console.log("No message received")
            return false;
        }
    }).catch(error => {
          console.log(error)
          return false;
    });
}

function updatelike(item){
    console.log(item)
    const id = parseInt(item.replace('like-button-',''));
    var param = document.querySelector(`#like-param-${id}`)
    var num_likes = document.querySelector(`#num-likes-${id}`)
    //var button = document.querySelector(`#${item.id}`)
    var img_path = document.querySelector(`#img-path-${id}`)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const like = "M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"
    const unlike = "m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"
    const request = new Request(
        "/likepost",
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        body: JSON.stringify({
            id: id,
            NewLikeData : param.value
        })
    })
    .then((response) => response.json())
    .then(result => {
        // Print result
        console.log(result);
        console.log(Object.keys(result))
        console.log(Object.keys(result) == "error")
        if (Object.keys(result) == "message"){
            if(param.value == "like"){
                img_path.setAttribute("d", like)
                param.value = "unlike"
                var likes = parseInt(num_likes.innerHTML)
                num_likes.innerHTML = likes+1
            }else{
                img_path.setAttribute("d",unlike)
                param.value = "like"
                var likes = parseInt(num_likes.innerHTML)
                num_likes.innerHTML = likes-1
            }
        }
        else{
            console.log("No message received")
            return false;
        }
    }).catch(error => {
          window.location = "/login"
          console.log(error)
          return false;
    });
}