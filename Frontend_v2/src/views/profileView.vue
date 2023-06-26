<template>
    <div class="container-fluid" >
        <div class="row">
        <div class="col-md-3 bg-light sidebar">
            <div class="sidebar-content" ref="leftSidebar">
                <!-- Left Sidebar -->
                <div class="card border-light mb-3" style="max-width: 20rem;" >
                    <div v-for="(userinfo, index) in usersData" :key="index">
                        <div class="card-header">
                            <span>
                                <h5><b>@{{ userinfo.userUsername }}</b></h5>
                            </span>
                            <span>
                                <button 
                                type="button" 
                                class="btn btn-success btn-sm d-inline-block position-absolute top-0" style="margin-left: 10.1rem; margin-top: 8px;" 
                                @click="follow(userinfo.userUsername)">
                                 Follow 
                                </button>
                            </span>
                            <span>
                                <button 
                                type="button" 
                                class="btn btn-secondary btn-sm d-inline-block position-absolute top-0 end-0"
                                style="margin-left: 10.9rem; margin-top: 8px;" 
                                @click="unfollow(userinfo.userUsername)">
                                 Unfollow 
                                </button>
                            </span>

                        </div>
                        <div class="card-body">
                            <h5 class="card-title">Name: <b>{{ userinfo.userName }}</b></h5>
                            <small> Number of blogs: <b>{{ userinfo.userNoBlog }}</b></small>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button type="button" class="btn btn-sm btn-outline-secondary" @click="showfollowers()">
                            <!-- <i class="bi bi-chat-dots"></i>
                             -->
                             #Followers: 
                            {{ this.followers.length }}

                        </button>
                        <div v-if="this.followers.length === 0">
                            <small> No followers </small>
                        </div>                        
                        <div v-if="showingfollowers && this.followers.length > 0" >
                            <ul>
                                <li v-for="(follower, index) in followers" :key="index">                           
                                    <a   @click="showUser(follower.username)"> @{{ follower.username }} </a>  
                                </li>
                            </ul> 
                        </div><br><br>
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
                                    <a   @click="showUser(follower.username)"> @{{ follower.username }} </a>
                                </li>
                            </ul>     
                        </div>
                    </div>     
                </div>
            </div><br>
        </div>
        </div>

        <div class="col-md-7 bg-light sidebar">
            <!-- Middle Sidebar -->
            <div class="container d-flex justify-content-between align-items-center">
                <div class="row">
                <div class="col-md-11">

                    <div v-for="(post, index) in posts" :key="index" class="card mb-3 border-dark"> 
                        <div class="card-body">
                            <div style="background-color: #e6e889;">
                                <span>
                                    <a class="card-title " style="text-decoration: none; font-size: larger;" v-if="post.blogArchive===false">@<b>{{ this.store.searchUsername }}</b>  &emsp; </a>
                                </span>
                        
                                <span>
                                    <small style="font-size: smaller; ">{{ post.blogCreation }} </small>
                                </span>

                            </div>

                            <h5 class="card-title border-bottom border-top mt-1">{{ post.blogTitle }}</h5>

                            <img v-if="post.blogImageURL" :src="`http://127.0.0.1:5000/image/${post.blogImageURL}`" class="card-img-top" alt="Post image">

                            <p class="card-text" style="text-align: justify;">{{ post.blogCaption }}</p>

                            <div class="d-flex justify-content-between align-items-center">

                            <div class="btn-group">
                                <button type="button" class="btn btn-sm btn-outline-secondary" disabled>
                                    <i class="bi bi-hand-thumbs-up" ></i>
                                    {{ post.likes }}
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-secondary" disabled>
                                    <i class="bi bi-hand-thumbs-down"></i>
                                    {{ post.dislikes }}
                                </button>

                                <button type="button" class="btn btn-sm btn-outline-secondary" @click="showComments(index)">
                                <i class="bi bi-chat-dots"></i>
                                {{ post.comments.length }}
                                </button>

                            </div>
                        
                        </div>
                    </div>
                    <div v-if="showingComments === index" class="card-footer">
                        <div v-for="(comment, index) in post.comments" :key="index" class="mb-2">
                            <div class="border-top border-bottom">
                                <span class="text-muted border-bottom"><b>@{{ comment.c_userUsername }}</b></span>
                                <p>&emsp; {{ comment.comment }}</p>
                            </div>
                        </div>
                    </div>
                    </div>
                </div>
                </div>
            </div>
        </div>
        <div class="col-md-2 bg-light sidebar">
            <!-- <div class="sidebar-content" ref="middleSidebar"> -->
            <br>
            <div class="d-flex position-relative">
                <button type="button" 
                class="btn btn-dark btn-sm position-absolute end-0 top-1"
                style="margin-top: -2%; margin-right:1% ;" 
                @click="home()">Go to home page</button>
            </div><br>  
        </div>
        </div>
    </div>
</template>

<script>

    import axios from "axios";
    import userStore from "../stores/counter.js";
    import dayjs from "dayjs";
    import relativeTime from "dayjs/plugin/relativeTime";
    dayjs.extend(relativeTime);

    export default{
        name: "searchUserComp",

        data(){
            return{
                usersData: [],
                posts: [],
                followers: [],
                following: [],
                showingfollowers: false,
                showingfollowing: false,
                new_User: "",
                showingComments: '',
            }
        },

        setup(){
            const store = userStore();
            return { store };
        },

        methods: {
            showfollowers(){
                this.showingfollowers = !this.showingfollowers;
            },

            home(){
                this.$router.push({ name: "Home Page" });
            },

            follow(name){
                const headers = {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + this.store.access_token,
                }
                axios.post(`http://localhost:5000/bloglite/relation/${name}`,{}, { headers })
                .then((response) => {
                    console.log(response);
                    if(response.data.id === 0)
                    this.followers.push({"username": this.store.userName});
                    alert(response.data.msg)

                })
                .catch((error) => {
                    console.log(error);

                });
            },
            unfollow(name){
                const headers = {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + this.store.access_token,
                }
                axios.delete(`http://localhost:5000/bloglite/relation/${name}`, { headers })
                .then((response) => {
                    console.log(response);
                    if(response.data.id === 0){
                        // apply the for loop in followers array and search the same user name and remove it
                        for(let i=0; i<this.followers.length; i++){
                            if(this.followers[i].username === this.store.userName){
                                this.followers.splice(i, 1);
                            }
                        }
                    }
                    alert(response.data.msg)

                })
                .catch((error) => {
                    console.log(error);

                });
            },

            showUser(name){
                this.store.show_User(name);

            },
            showfollowings(){
                this.showingfollowing = !this.showingfollowing;
            },
            showComments(index) {
                // this.showingComments = !this.showingComments;
                if(this.showingComments === index){
                    this.showingComments = '';
                }else{
                    this.showingComments = index;
                }
            },
        },

        computed: {
            showCom(){
                return this.showingComments !== '';
            }
        },

        // life cycle hooks
        
        beforeMount(){
            if(!this.store.isLoggedIn){
                this.$router.push({ name: "login" });
            }
        },

        mounted(){

            const headers = {
                "Content-Type": "application/json",
                Authorization: "Bearer " + this.store.access_token,
            };
            axios.get(`http://localhost:5000/bloglite/profile/${this.store.searchUsername}`,  { headers })
            .then((response) => {
                this.usersData = response.data.profile_feed.userData;
                this.posts = response.data.profile_feed.blogs;
                this.followers = response.data.profile_feed.followers;
                this.following = response.data.profile_feed.following;
                // change the date format
                this.posts.forEach((post) => {
                    post.blogCreation = dayjs(post.blogCreation).fromNow();
                });
                // console.log(this.usersData);
                console.log(this.followers);
            })
            .catch((error) => {
                console.log(error);
            }); 



            
        },


        
    }


</script>

<style scoped>
.sidebar {
    height: 100vh;
    overflow: auto;
    position: relative;
  }
  
  .sidebar-content {
    height: 100%;
    overflow-y: auto;
    padding: 1rem;
  
    /* Thin Scrollbar */
    scrollbar-width: thin;
    scrollbar-color: #c4c4c4 #f2f2f2;
  }
  
  .sidebar-content::-webkit-scrollbar {
    width: 8px;
  }
  
  .sidebar-content::-webkit-scrollbar-track {
    background-color: #f2f2f2;
  }
  
  .sidebar-content::-webkit-scrollbar-thumb {
    background-color: #c4c4c4;
  }
  
  .sidebar-content::-webkit-scrollbar-thumb:hover {
    background-color: #aaa;
  }
  .card-footer{
    max-height: 300px;
    overflow-y: auto;
  }

</style>