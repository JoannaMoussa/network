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
    edit_icons = document.querySelectorAll('[id^="edit-icon"]')
    if (edit_icons) {
        edit_icons.forEach(edit_icon => {
            edit_icon.addEventListener("click", () => {
                // get the post id and post content
                let post_id = edit_icon.dataset.postid;
                let post_content = document.querySelector(`#content-${post_id}`).innerHTML;

                // Hide the container of the like/edit icons and the post content container
                let like_edit_container = document.querySelector(`#like-edit-container-${post_id}`);
                like_edit_container.style.display = "none";
                let content_container = document.querySelector(`#content-${post_id}`);
                content_container.style.display = "none";

                post_details_container = document.querySelector(`#post-details-${post_id}`);
                // Create text area                
                text_area = document.createElement("textarea");
                text_area.value = post_content;
                post_details_container.append(text_area);
                // Create save btn
                save_btn = document.createElement("button");
                save_btn.setAttribute("type", "button");
                save_btn.classList.add("btn", "btn-sm", "btn-primary", "mt-1")
                save_btn.innerHTML = "Save";
                post_details_container.append(save_btn);
                
                // Add click event listner to save btn
                save_btn.addEventListener("click", () => {
                    let edited_content = text_area.value.trim();
                    if (edited_content == "") {
                        create_msg("The post content can not be empty!", true)
                    }
                    else if (edited_content.length > 280) {
                        create_msg("You exceeded the maximum character length that is 280.", true)
                    }
                    else {
                        fetch("/saveEditedPost", {
                            method: "PUT",
                            body: JSON.stringify({
                                "post_id": post_id,
                                "text_area_content": edited_content
                            })
                        })
                        .then(response => {
                            return response.json().then(json => {
                                return response.ok ? json.message : Promise.reject(json.error);
                            })
                        })
                        .then(success_msg => {
                            text_area.remove();
                            save_btn.remove();
                            like_edit_container.style.display = "flex";
                            content_container.innerHTML = edited_content;
                            content_container.style.display = "block";
                            create_msg(success_msg, false)
                        })
                        .catch(error_msg => {
                            create_msg(error_msg, true)
                        })
                    }
                })
            })
        })
    }
})