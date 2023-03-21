## CS50's Web Programming with Python and JavaScript

# Project 4 - Network

This project consists of making a social network that allows users to make posts, follow other users, and “like” posts.

The application has the following features:

1. **All posts page:** It's where users can see all posts from all users, with the most recent posts first.
    * Each post includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has.

1. **Following:** This page is only available to users who are **signed in**. It's where users see all posts made by users that the current user follows.

1. **New Post:** From the "All posts" page or from the "Following page", users who are **signed in** are able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

1. **Profile Page:** Clicking on a username loads that user’s profile page. This page displays:
    * The number of followers the user has, as well as the number of people that the user follows.
    * All of the posts for that user, in reverse chronological order.
    * For any other user who is **signed in**, this page also displays a `Follow` or `Unfollow` button that will let the current user toggle whether or not they are following this user’s posts. This only applies to any “other” user: a user can not follow themselves.

1. **Pagination:** On any page that displays posts, posts are only displayed 10 on a page. A “Next” button takes the user to the next page of posts. A “Previous” button takes the user to the previous page of posts as well.

1. **Edit Post:** Users are able to click an “Edit” button on any of their **own** posts to edit that post.
    * When a user clicks `Edit`, the content of their post is replaced with a textarea where the user can edit the content.
    * The user is then able to `Save` the edited post.
    * The user is able to `Cancel` the modifications made, in that case the content remains the same.

1. **Like and Unlike:** Users are able to click a button on any post to toggle whether or not they “like” that post.

 Using JavaScript, the following functionalities are achieved without requiring a reload of the entire page:
* Follow and Unfollow
* Edit a Post
* Like and Unlike a Post