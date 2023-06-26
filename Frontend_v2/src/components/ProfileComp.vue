<template>
    <div class="container d-flex justify-content-between align-items-center">
        <div class="row">
            <div class="card border-light mb-3 " >
                <div class="card-header">
                    <span class="text-center">
                        <h4><b>My Profile</b></h4>
                    </span>
                    <span class="dropdown d-inline-block position-absolute top-0 end-0">
                        <button 
                            class="btn   d-flex align-items-end" 
                            type="button" id="dropdownMenuButton" 
                            data-bs-toggle="dropdown" 
                            aria-haspopup="true" 
                            aria-expanded="false">
                                <i class="bi bi-three-dots-vertical"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                            <li >
                                <a class="dropdown-item"  
                                  
                                data-bs-toggle="modal" data-bs-target="#update_password">
                                    Update Password
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" 
                                
                                data-bs-toggle="modal"
                                
                                data-bs-target="#delete_user_con">
                                    Delete Profile
                                </a>
                            </li>
                        </ul>
                    </span>
                </div>
                <div class="card-body">
                    <small>Name:&emsp; <b>{{ this.store.name }}</b></small><br>
                    <small>Username:&emsp; <b>@{{ this.store.userName }}</b> </small><br>
                    <small> Number of blogs:&emsp; <b>{{ this.store.noblogs }}</b></small><br>
                </div>
                <div class="card-footer">
                    <button type="button" class="btn btn-sm btn-outline-secondary" @click="showfollowers()">
                        #Followers: 
                        {{ this.followers.length }}
                    </button><br>
                    <div v-if="this.followers.length === 0">
                        <small> No followers </small>
                    </div>
                    <div v-if="showingfollowers && this.followers.length > 0" >
                        <ul>
                            <li v-for="(follower, index) in followers" :key="index">
                                <div>
                                    <span>
                                        <a  type="button"  @click="showUser(follower.username)"> @{{ follower.username }} </a>
                                    </span>
                                    <span>
                                        <button
                                        type="button"
                                        class="btn btn-success btn-sm d-inline-block text-right "
                                        style="margin-left: 10.9rem;"
                                        @click="follow(follower.username)">
                                            follow
                                        </button>
                                    </span>
                                </div>
                            </li>
                        </ul>   
                    </div><br>             
                    <div>
                        <button type="button" class="btn btn-sm btn-outline-secondary" @click="showfollowings()">
                            #Followings: 
                            {{ this.following.length }}
                        </button>

                        <div v-if="this.following.length === 0">
                            <small> No followings </small>
                        </div>
                        <div v-if="showingfollowing && this.following.length > 0" >
                            <ul>
                                <li v-for="(follower, index) in following" :key="index">                   
                                    <span>
                                        <a  type="button"  @click="showUser(follower.username)"> @{{ follower.username }} </a>
                                    </span>
                                    <span>
                                        <button
                                        type="button"
                                        class="btn btn-secondary btn-sm d-inline-block text-right"
                                        style="margin-left: 10.9rem;"
                                        
                                        @click="unfollow(follower.username, index)">
                                            unfollow
                                        </button>
                                    </span>                   
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div>
                        <br>
                        <!-- clicable link which is connected with modal and provide the option to change the default format report -->
                        <a href="#" data-bs-toggle="modal" data-bs-target="#changeReport">Change monthly report format</a>


                    </div><br> 
                    <div class="position-relative">
                        <!-- create a button for create blog -->
                        <button @click="CreateBlog = true" type="button" class="btn btn-success position-absolute end-0 bottom-0" data-bs-toggle="modal" data-bs-target="#createBlog">
                        Create Blog
                        </button>
                    </div> 
                </div>
            </div><br>

            <div class="col-md-11">
                <div v-for="(post, index) in posts" :key="index" class="card mb-3 border-dark" >        
                    <div class="card-body" >
                        <div class="d-flex">
                            <span>
                                <p class="card-title" style="text-decoration: none; font-size: medium; color: red;" v-if="post.blogArchive === true">private &emsp; </p> 
                                <p class="card-title" style="text-decoration: none; font-size: medium; color: blue;" v-if="post.blogArchive === false">public&emsp; </p>
                            </span>
                
                            <span>
                                <small style="font-size: smaller;">{{post.blogCreation }} </small>
                            </span>
                            <span class="dropdown d-inline-block position-absolute top-1 end-0">
                                <button 
                                    class="btn   d-flex align-items-end" 
                                    type="button" id="dropdownMenuButton" 
                                    data-bs-toggle="dropdown" 
                                    aria-haspopup="true" 
                                    aria-expanded="false">
                                        <i class="bi bi-three-dots-vertical"></i>
                                </button>
                                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                                    <li >
                                        <a class="dropdown-item"  
                                        @click="editBlog(post.blogId, index)"  
                                        data-bs-toggle="modal" data-bs-target="#updateBlog">
                                         Edit
                                        </a>
                                    </li>
                                    <li>
                                        <a class="dropdown-item" 
                                        @click="deletePost(post.blogId, index)"
                                        data-bs-toggle="modal" data-bs-target="#delete_confirmation">
                                            Delete
                                        </a>
                                    </li>
                                    <li>
                                        <a class="dropdown-item" href="#"
                                        @click="download(post.blogId)">
                                            Download
                                        </a>
                                    </li>
                                </ul>
                            </span>
                        </div>
                        <h4 class="card-title mt-2"
                        style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; font-size: 20px;">
                            {{ post.blogTitle }}
                        </h4>
                        <img v-if="post.blogImageURL" :src="`http://127.0.0.1:5000/image/${post.blogImageURL}`" 
                        class="card-img-top" alt="Post image">

                        <p  class="card-text" >
                            {{ post.blogCaption }}
                        </p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="btn-group">
                                <button type="button" class="btn btn-sm btn-outline-secondary" disabled>
                                    <i class="bi bi-hand-thumbs-up"></i>
                                    {{ post.likes }}
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-secondary" disabled>
                                    <i class="bi bi-hand-thumbs-down"></i>
                                    {{ post.dislikes }}
                                </button>

                                <button type="button" 
                                class="btn btn-sm btn-outline-secondary" 
                                @click="showComments(index)">
                                    <i class="bi bi-chat-dots"></i>
                                    {{ post.comments.length }}
                                </button>
                            </div>
                        </div>
                    </div>
                    <div v-if="showingComments === index" class="card-footer">
                        <div style="position: sticky; top: 0; z-index: 1;" >
                            <form @submit.prevent="addComment(post, post.blogId)" class="mb-3"  >
                            <div class="input-group">
                                <input type="text" 
                                class="form-control" placeholder="Add a comment" 
                                v-model="post.newComment" required>
                                <button type="submit" 
                                class="btn btn-outline-secondary">
                                Post
                                </button>
                            </div>
                            </form>
                        </div>
                        

                        <div v-for="(comment, c_index) in post.comments" 
                        :key="c_index" 
                        class="mb-2">
                            <div class="border-top border-bottom">
                                <span class="text-muted border-bottom">
                                    <b>@{{ comment.c_userUsername }}</b>
                                </span>
                                <span class="dropdown d-inline-block position-relative">
                                    <button 
                                        class="btn   d-flex align-items-end" 
                                        type="button" id="dropdownMenuButton" 
                                        data-bs-toggle="dropdown" 
                                        aria-haspopup="true" 
                                        aria-expanded="false"
                                        v-if="comment.c_userUsername === this.store.userName">
                                            <i class="bi bi-three-dots-vertical"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                                        <li >
                                            <a class="dropdown-item"  
                                            @click="editComment(index,comment.commentId, c_index)"
                                            data-bs-toggle="modal" data-bs-target="#update_Comment">
                                                Update Comment
                                            </a>
                                        </li>
                                        <li>
                                            <a class="dropdown-item"                                            
                                            data-bs-toggle="modal"
                                            @click="deleteComment(post, comment.commentId, c_index)"                                            
                                            >
                                                Delete Comment
                                            </a>
                                        </li>
                                    </ul>
                            </span>

                            </div>

                            <div>
                                <p>&emsp; {{ comment.comment }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- create blog template -->
    <blogCreate v-if="showCreateBlog" @new_blog="new_blog_created"/>
    <!-- update blog template -->
    <updateBlog v-if="true" :editBlogId="this.blogId" @updatedBlog="upd_blog"></updateBlog>
    <!-- update blog password template -->
    <update_password v-if="true" ></update_password>
    <!-- delete user template -->
    <delete_user v-if="true" ></delete_user>



<!-- Delete Confirmation -->

    <div class="modal fade" id="delete_confirmation" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Delete Confirmation</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                Are you sure you want to delete this blog?
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="delete_con">Delete</button>
                <!-- the "data-bs-dismiss" attribute tells Bootstrap to close the modal when this button is clicked -->
            </div>
            </div>
        </div>
    </div>

    <!-- Update Comment -->

    <div class="modal fade" id="update_Comment" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Update Comment</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form class="form" role="form" autocomplete="off" >
                    <div class="mb-3">
                        <label for="u_comment" class="form-label">Comment</label>
                        <textarea class="form-control" id="u_comment" rows="3" v-model="update_comment"></textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click="edit_Comment">Update</button>
                    </div>
                </form>
                
            </div>
            
            </div>
        </div>
    </div>

    <!-- Change Report Format -->

    <div class="modal fade" id="changeReport" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Monthly Report Format</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                Update the monthly report format?
                
                <div>
                  <input class="form-check-input" type="radio" name="exampleRadios" id="pdf" value="pdf" v-model="selectedOption">
                  <label class="form-check-label" for="pdf">
                    PDF
                  </label>
                </div>
                  <div>
                    <input class="form-check-input" type="radio" name="exampleRadios" id="html" value="html" v-model="selectedOption">
                    <label class="form-check-label" for="html">
                      HTML
                    </label>
                  </div>

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="changeFormat">Update</button>
                <!-- the "data-bs-dismiss" attribute tells Bootstrap to close the modal when this button is clicked -->
            </div>
            </div>
        </div>
    </div>
</template>


<script>

import axios from "axios";
import userStore from "../stores/counter.js";
import updateBlog from "./updateBlogComp.vue";
import update_password from "./update_password.vue";
import delete_user from "./delete_user_con.vue";
import blogCreate from "./blogCreate.vue";
import dayjs from 'dayjs';
import relativeTime from "dayjs/plugin/relativeTime";
dayjs.extend(relativeTime);


export default {
    name: "ProfileComp",

    setup() {
    const store = userStore();
    return { store };
    },

    

    data() {
        return {
            usersData: [],
            posts: [],
            followers: [],
            following: [],
            showingfollowers: false,
            showingfollowing: false,
            showingComments: '',
            id: "",
            index: "",
            selectedOption: "",
            blogId: "",
            edit_index: "",
            showCreateBlog: true,
            commentIndex: "",
            editComId: "",
            update_comment: "",
            CPindex: "",
   
        };
    },


    components: {
        updateBlog,
        update_password,
        delete_user,
        blogCreate,
    },

    mounted() {
        const headers = { 
            "Content-Type": "application/json",
            Authorization: "Bearer " + this.store.access_token,
        };
        
        axios.get(`http://localhost:5000/bloglite/profile/${this.store.userName}`, { headers })
        .then((response) => {
                // this.usersData = response.data.profile_feed.userData;
                this.posts = response.data.blogs;
                
                this.followers = response.data.followers;
                this.following = response.data.following;
                // change the this.posts.blogCreation to dayjs
                this.posts.forEach(post => {
                    post.blogCreation = dayjs(post.blogCreation).fromNow();
                });

                // console.log(this.usersData);
                console.log(this.followers);
                console.log(response);
            })
            .catch((error) => {
                console.log(error);
            });     
    },

    methods: {
        // Required methods for the component
        new_blog_created(blog) {
            console.log("Data from child component: ", blog);
            this.posts.unshift(blog);
            // this.posts.unshift(this.posts.splice(this.edit_index+1, 1)[0]);
            // sfit it to the top of the list and remove the indexed placed blog

        },
        CreateBlog() {
            this.showCreateBlog = false;
        },
        upd_blog(updated_blog){
            console.log("Data from child component updated: ", updated_blog);
            this.posts[this.edit_index].blogArchive = updated_blog.blogArchive;
            this.posts[this.edit_index].blogTitle = updated_blog.blogTitle;
            this.posts[this.edit_index].blogCaption = updated_blog.blogCaption;
            this.posts[this.edit_index].blogImageURL = updated_blog.blogImageURL;
            this.posts[this.edit_index].blogCreation = dayjs(updated_blog.blogCreation).fromNow();
            // shift this blog to the 0th position in the array
            this.posts.unshift(this.posts.splice(this.edit_index, 1)[0]);
            // console.log("working updated_blog")

        },

        showComments(index) {
            if(this.showingComments === index) {
                this.showingComments = '';
            } else {
                this.showingComments = index;
            }
            // this.showingComments = !this.showingComments;
            // this.showingComments = cIndex;
        },
        addComment(post, id) {
            const headers = { 
            "Content-Type": "application/json",
            Authorization: "Bearer " + this.store.access_token,
            };

            const data = {
            "comment": post.newComment,
            };

            axios.post(`http://localhost:5000/bloglite/blog/comment/${id}`, data, { headers })
            .then((response) => {
            // console.log(response.data);
            alert(response.data.msg)
            post.comments.unshift({
                c_userUsername: this.store.userName,
                comment: post.newComment,
                commentId: response.data.commentId,
            });
            console.log(response.data.commentId)
            post.newComment = '';
            }).catch(() => {
            alert("something went wrong, please try again")
            });
        },

        editComment(index,commentId, cIndex) {
            this.commentIndex = cIndex;
            this.editComId = commentId;
            this.CPindex = index;
            console.log(index)
            console.log(commentId)
            console.log(this.CPindex)
        },
        edit_Comment(){
            const headers = { 
            "Content-Type": "application/json",
            Authorization: "Bearer " + this.store.access_token,
            };

            const data = {
            "comment": this.update_comment,
            };

            axios.put(`http://localhost:5000/bloglite/blog/comment/${this.editComId}`, data, { headers })
            .then((response) => {
            // console.log(response.data);
                this.posts[this.CPindex].comments[this.commentIndex].comment = this.update_comment
                this.posts[this.CPindex].comments.unshift(this.posts[this.CPindex].comments[this.commentIndex])
                this.posts[this.CPindex].comments.splice(this.commentIndex + 1, 1)
                alert(response.data.msg)
                this.commentIndex = '';
                this.editComId = '';
                this.update_comment = '';
            }).catch((error) => {
                console.log(error)
                alert("something went wrong, please try again")
            });

        },



        deleteComment(post,  commentId, cIndex) {
            const headers = { 
            "Content-Type": "application/json",
            Authorization: "Bearer " + this.store.access_token,
            };

            axios.delete(`http://localhost:5000/bloglite/blog/comment/${commentId}`, { headers })
            .then((response) => {
            // console.log(response.data);
            alert(response.data.msg)
            post.comments.splice(cIndex, 1);
            }).catch(() => {
            alert("something went wrong, please try again")
            });
        },

        editBlog(id, index){
            this.blogId = id;
            this.edit_index = index;
            // console.log('edit blog id' + this.blogId)          
        },

        deletePost(id, index) {
            this.id = id;
            this.index = index;     
        },

        delete_con()  {
            const headers = { 
                "Content-Type": "application/json",
                Authorization: "Bearer " + this.store.access_token,
            };
        
            axios.delete(`http://localhost:5000/bloglite/blog/${this.id}`, { headers })
            .then((response) => {
                this.posts.splice(this.index, 1);
                this.store.delete_blog();
                alert(response.data.msg);
            })
            .catch((error) => {
                console.log(error);
            });
        },

        changeFormat(){
            const headers = { 
                "Content-Type": "application/json",
                Authorization: "Bearer " + this.store.access_token,
            };
            
            const data = {
                "reportFormat": this.selectedOption,
            }
            axios.put("http://localhost:5000/bloglite/user/report",data, { headers })
            .then((response) => {
                alert(response.data.msg);
                this.selectedOption = "";
            })
            .catch((error) => {
                console.log(error);
            });
        },

        showfollowings(){
            this.showingfollowing = !this.showingfollowing;
        },
        showfollowers(){
            this.showingfollowers = !this.showingfollowers;
        },

        follow(name){
            const headers = {
                "Content-Type": "application/json",
                Authorization: "Bearer " + this.store.access_token,
            }
            axios.post(`http://localhost:5000/bloglite/relation/${name}`,{}, { headers })
            .then((response) => {
                console.log(response);
                if(response.data.id === 0){
                    this.following.push({"username": name});
                }
                alert(response.data.msg)

            })
            .catch((error) => {
                console.log(error);

            });
        },
        unfollow(name, index){
            const headers = {
                "Content-Type": "application/json",
                Authorization: "Bearer " + this.store.access_token,
            }
            axios.delete(`http://localhost:5000/bloglite/relation/${name}`, { headers })
            .then((response) => {
                console.log(response);
                if(response.data.id === 0){
                    this.following.splice(index, 1);
                }
                alert(response.data.msg)

            })
            .catch((error) => {
                console.log(error);

            });
        },

        showUser(name){
            this.store.show_User(name);
            this.$router.push("/profile");
        },

        async exportblog(id){
            return await fetch(
                `http://localhost:5000/export/blog/${id}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + this.store.access_token,

                    },

                }

            )
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                alert("Exporting blog");
                console.log(data.taskID)
                return data.taskID;
            })
            .catch((error) => {
                alert("Error exporting blog")
                console.log(error);
            });
            
        },


        async checkStatus(taskID){
            const headers = {
                "Content-Type": "application/json",
                Authorization: "Bearer " + this.store.access_token,
            }
            let response = await axios.get(`http://localhost:5000/export/blog/status/${taskID}`, { headers });

            if(response.status === 200){
                const data = await response.data;
                console.log(data);
                // alert("Staus: Exporting" );
                // console.log("Status: Exporting")
                // console.log(data.status)
                return data.status;
            }else{
                alert("Error exporting blog");
                // console.log("Status: Error exporting blog");
            }
        },


        async download(id){
            let taskID = await this.exportblog(id);
            
            if(taskID){
                console.log(taskID)
                setTimeout(() => {
                    let interval = setInterval(async() =>{
                        let status = await this.checkStatus(taskID);
                        console.log(status)
                        if(status === "SUCCESS"){
                            alert("Downloading started");
                            let a = document.createElement("a");
                            a.href = `http://localhost:5000/bloglite/download/blog/${id}`;
                            a.click();
                            clearInterval(interval);

                        }else if(status === "FAILURE"){
                            alert("Download failed");
                            clearInterval(interval);
                        }else if(status === "PENDING"){
                            alert("Download is taking longer than expected. Please try again later");
                            clearInterval(interval);
                        }
                    }, 3000); // 3 seconds
                10000}); // 1 minutes

            }else {
                alert("Error exporting blog");
            }
        
            },
    },
    computed: {
        showCom() {
            return this.showingComments !== '';
        },
    },
}


</script>

<style scoped>
.card-footer {
    /* display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1.25rem;
    background-color: rgba(0, 0, 0, 0.03);
    border-top: 1px solid rgba(0, 0, 0, 0.125); */
    max-height: 300px;
    overflow-y: auto;
}
</style>
  
  
<!-- data-bs-target="#delete_comment_con" -->