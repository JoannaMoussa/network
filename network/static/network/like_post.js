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
                let post_id = heart_icon.dataset.postid;
                fetch("/liketoggle", {
                    method: "PUT",
                    body: JSON.stringify({
                        "post_id": post_id
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
                        heart_icon.classList.remove("bi-heart-fill");
                        heart_icon.classList.remove("heart_fill_icon");
                        heart_icon.classList.add("bi-heart");
                        likes_count_container.innerHTML = json.likes_count;
                        create_msg(json.message, false);
                    }
                    else {
                        heart_icon.classList.remove("bi-heart");
                        heart_icon.classList.add("bi-heart-fill");
                        heart_icon.classList.add("heart_fill_icon");
                        likes_count_container.innerHTML = json.likes_count;
                        create_msg(json.message, false);
                    }
                })
                .catch(error_msg => {
                    create_msg(error_msg, true);
                })
            })
        })
    }
})