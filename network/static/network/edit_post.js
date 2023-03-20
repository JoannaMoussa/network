// This function displays the message in a modal (=pop up window)
function create_msg(msg, is_error){
    let popup_msg = document.querySelector("#popup-msg");
    popup_msg.style.display = "flex";
    if (popup_msg.classList.contains("popup_animation")) {
        // restart animation
        popup_msg.style.animation = "none";
        popup_msg.offsetHeight; // trigger reflow
        popup_msg.style.animation = null;
    }
    else {
        popup_msg.classList.add("popup_animation");
    }
     
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
  }

let edit_allowed = true;

document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to the popup message and its close btn
    let popup_msg = document.querySelector("#popup-msg");
    popup_msg.addEventListener("animationend", () => {
        popup_msg.classList.remove("popup_animation");
        popup_msg.style.display = "none";
    })
    let close_btn = document.querySelector("#close-btn");
    close_btn.addEventListener("click", () => {
        popup_msg.style.display = "none";
    })
    
    edit_icons = document.querySelectorAll('[id^="edit-icon"]')
    if (edit_icons) {
        edit_icons.forEach(edit_icon => {
            edit_icon.addEventListener("click", () => {
                if (edit_allowed) {
                    edit_allowed = false;
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
                    let text_area = document.createElement("textarea");
                    text_area.value = post_content;
                    post_details_container.append(text_area);

                    // Create container for save btn and cancel btn
                    let save_cancel_container = document.createElement("div");
                    save_cancel_container.classList.add("mt-1");

                    // Create cancel button
                    let cancel_btn = document.createElement("button");
                    cancel_btn.setAttribute("type", "button");
                    cancel_btn.classList.add("btn", "btn-sm", "btn-primary", "mr-2");
                    cancel_btn.innerHTML = "Cancel";
                    save_cancel_container.append(cancel_btn);

                    // Add click event listner to cancel btn
                    cancel_btn.addEventListener("click", () => {
                        edit_allowed = true;
                        text_area.remove();
                        save_cancel_container.remove();
                        content_container.innerHTML = post_content;
                        content_container.style.display = "block";
                        like_edit_container.style.display = "flex";
                    })

                    // Create save btn
                    let save_btn = document.createElement("button");
                    save_btn.setAttribute("type", "button");
                    save_btn.classList.add("btn", "btn-sm", "btn-primary");
                    save_btn.innerHTML = "Save";
                    save_cancel_container.append(save_btn);

                    post_details_container.append(save_cancel_container);
                    
                    // Add click event listner to save btn
                    save_btn.addEventListener("click", () => {
                        let edited_content = text_area.value.trim();
                        if (edited_content == "") {
                            create_msg("Careful! The post content can not be empty!", true)
                        }
                        else if (edited_content.length > 280) {
                            create_msg("Careful! You exceeded the maximum character length that is 280.", true)
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
                                edit_allowed = true;
                                text_area.remove();
                                save_cancel_container.remove();
                                like_edit_container.style.display = "flex";
                                content_container.innerHTML = edited_content;
                                content_container.style.display = "block";
                                create_msg(success_msg, false)
                            })
                            .catch(error_msg => {
                                create_msg(error_msg, true);
                            })
                        }
                    })
                }
                // if edit is not allowed (bcz there's another edit in progress)
                else {
                    create_msg("Finish the current edit to proceed.", true) 
                } 
            })
        })
    }
})