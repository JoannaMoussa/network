// This function displays the message in a modal (=pop up window)
function create_msg(msg, is_error){
    let popup_msg = document.querySelector("#popup-msg");
    popup_msg.style.display = "flex";
    if (popup_msg.classList.contains("popup_animation")) {
        popup_msg.classList.remove("popup_animation");
    }
    popup_msg.classList.add("popup_animation");
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
    
    profile_username = document.querySelector("#profile-username").dataset.username

    // Add click event listener to the unfollow btn
    unfollow_btn = document.querySelector('#unfollow-btn');
    if (unfollow_btn) {
        unfollow_btn.addEventListener("click", () => {
            fetch("/unfollow", {
                method: "DELETE",
                body: JSON.stringify({
                    "profile_username": profile_username
                  })
            })
            .then(response => {
                return response.json().then(json => {
                    return response.ok ? json : Promise.reject(json.error);
                });
            })
            .then(json_response => {
                // Display the follow btn instead of the unfollow btn
                document.querySelector("#unfollow-btn").style.display = "none";
                document.querySelector("#follow-btn").style.display = "block";
                // Update the followers count in the profile page
                if (json_response.followers_count == 1) {
                    document.querySelector("#followers-count").innerHTML = `<strong>${json_response.followers_count}</strong> Follower`
                }
                else {
                    document.querySelector("#followers-count").innerHTML = `<strong>${json_response.followers_count}</strong> Followers`
                }
                // Success message to the user
                create_msg(json_response.message, false)
            })
            .catch(error_msg => {
                // Error message to the user
                create_msg(error_msg, true)
              })
        })
    }

    // Add click event listener to the follow btn
    follow_btn = document.querySelector('#follow-btn');
    if (follow_btn) {
        follow_btn.addEventListener("click", () => {
            fetch("/follow", {
                method: "POST",
                body: JSON.stringify({
                    "profile_username": profile_username
                })
            })
            .then(response => {
                return response.json().then(json => {
                    return response.ok ? json : Promise.reject(json.error)
                })
            })
            .then(json_response => {
                // Display the unfollow btn instead of the follow btn
                document.querySelector("#unfollow-btn").style.display = "block";
                document.querySelector("#follow-btn").style.display = "none";

                // Update the followers count in the profile page
                if (json_response.followers_count == 1) {
                    document.querySelector("#followers-count").innerHTML = `<strong>${json_response.followers_count}</strong> Follower`
                }
                else {
                    document.querySelector("#followers-count").innerHTML = `<strong>${json_response.followers_count}</strong> Followers`
                }

                // Success message to the user
                create_msg(json_response.message, false)
            })
            .catch(error_msg => {
                // Error message to the user
                create_msg(error_msg, true)
            })
        })
    }
})