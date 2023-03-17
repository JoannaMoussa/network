// This function displays the message in a modal (=pop up window)
function create_msg(msg, is_error){
    let popup_msg = document.querySelector("#popup-msg");
    popup_msg.style.display = "flex";
    if (popup_msg.classList.contains("popup_animation")) {
        popup_msg.classList.remove("popup_animation")
    }
    popup_msg.classList.add("popup_animation")
    popup_msg.addEventListener("animationend", () => {
        popup_msg.classList.remove("popup_animation");
        popup_msg.style.display = "none";
    })
    if (is_error){ 
        popup_msg.classList.remove("popup_success_msg");
        popup_msg.classList.add("popup_error_msg");
    }
    else {
        popup_msg.classList.remove("popup_error_msg");
        popup_msg.classList.add("popup_success_msg");
    }
    let popup_text = document.querySelector("#popup-text");
    popup_text.innerHTML = msg;

    let close_btn = document.querySelector("#close-btn");
    close_btn.addEventListener("click", () => {
        popup_msg.style.display = "none";
    })
  }

document.addEventListener('DOMContentLoaded', function() {
    heart_icons = document.querySelectorAll('[id^="heart"]');
    if (heart_icons) {
        heart_icons.forEach(heart_icon => {
            heart_icon.addEventListener("click", () => {
                if (! heart_icon.classList.contains("like_animation")) {
                    let post_id = heart_icon.dataset.postid;
                    // ui_like_state is a variable that will indicate the like state in the front end.
                    // in other terms, as per the user, he's one of the likers of the post or not?
                    let ui_like_state;
                    if (heart_icon.dataset.likestate == "liked"){
                        ui_like_state = true;
                    }
                    else if (heart_icon.dataset.likestate == "notliked"){
                        ui_like_state = false;
                    }
                    else {
                        create_msg("Erorr processing request. Please reload page.", true);
                    }
                    fetch("/liketoggle", {
                        method: "PUT",
                        body: JSON.stringify({
                            "post_id": post_id,
                            "ui_like_state": ui_like_state
                        })
                    })
                    .then(response => {
                        return response.json().then(json => {
                            return response.ok ? json : Promise.reject(json.error);
                        })
                    })
                    .then(json => {
                        let likes_count_container = document.querySelector(`#likes-count-${post_id}`)
                        if (json.like == false){
                            heart_icon.classList.remove("red_heart");
                            likes_count_container.innerHTML = json.likes_count;
                            heart_icon.dataset.likestate = "notliked";
                        }
                        else {
                            heart_icon.classList.add("like_animation");
                            likes_count_container.innerHTML = json.likes_count;
                            heart_icon.dataset.likestate = "liked";
                            heart_icon.addEventListener("animationend", () => {
                                heart_icon.classList.remove("like_animation");
                                heart_icon.classList.add("red_heart");
                            })
                        }
                    })
                    .catch(error_msg => {
                        create_msg(error_msg, true);
                    })
                } 
            })
        })
    }
})