// This function creates an error message div with bootstrap classes for styling.
// TODO: make the message dismissible
function create_error_msg(error_msg){
    const error_div = document.createElement('div');
    error_div.classList.add('alert','alert-danger');
    error_div.setAttribute('role', 'alert');
    error_div.innerHTML = error_msg;
    document.querySelector('#js-message').append(error_div);
  }


// This function creates a success message div with bootstrap classes for styling.
// TODO: make the message dismissible
function create_success_msg(success_msg){
    const success_div = document.createElement('div');
    success_div.classList.add('alert','alert-success');
    success_div.setAttribute('role', 'alert');
    success_div.innerHTML = success_msg;
    document.querySelector('#js-message').append(success_div);
  }


document.addEventListener('DOMContentLoaded', function() {
    unfollow_btn = document.querySelector('#unfollow-btn');
    if (unfollow_btn) {
        unfollow_btn.addEventListener("click", () => {
            profile_username = document.querySelector("#profile-username").dataset.username
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
                create_success_msg(json_response.message)
            })
            .catch(error_msg => {
                // Error message to the user
                create_error_msg(error_msg)
              })
        })
    }
})