<template >

  <div class="container d-flex justify-content-between align-items-center">
    <div class="row">
      <div class="col-md-11">

        <div v-if="this.posts.length === 0">
            <h5>You are not following any user</h5>
        </div>

        <div v-if="this.posts.length > 0">
            <h4 style="text-align: center;"><b>My Feeds</b></h4>
        </div> 

        <div v-for="(post, index) in posts" :key="index" class="card mb-3 border-dark"> 
        
          <div class="card-body">

            <div class="border-top border-bottom" style="background-color: #e6e889;">
              
              <span >
                <a class="card-title" 
                type="button" 
                style="text-decoration: none; font-size: large;"
                @click="showUser(post.f_userUsername)">
                <b>@{{ post.f_userUsername }}</b>
                &emsp; </a>
              </span>

              <span>
                <small>
                  {{ post.blogCreation }}
                </small>
              </span>

            </div>

            <h5 class="card-title mt-2 ml-1"
            style="font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; font-size: 20px;"
            >
              {{ post.blogTitle }}
            </h5>

            <img v-if="post.blogImageURL" :src="`http://127.0.0.1:5000/image/${post.blogImageURL}`" class="card-img-top" alt="Post image">

            <p class="card-text" style="font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif; font-size: 17px; text-align: justify,;">
              {{ post.blogCaption }}
            </p>

            <div class="d-flex justify-content-between align-items-center">
              <div class="btn-group">
                <!-- button for likes and dislikes -->
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="like(post.blogId, index)">
                  <i class="bi bi-hand-thumbs-up"></i>
                  {{ post.likes }}
                </button>
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="dislike(post.blogId, index)">
                  <i class="bi bi-hand-thumbs-down"></i>
                  {{ post.dislikes }}
                </button>

                <!-- button for comments -->
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="showComments(index)">
                  <i class="bi bi-chat-dots"></i>
                  {{ post.comments.length }}
                </button>
              </div>

            </div>
          </div>
          <div v-if="showingComments === index" class="card-footer">
            <form @submit.prevent="addComment(post, post.blogId)" class="mb-3" style="position: sticky; top: 0; z-index: 1;">
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
            <div class="mb-2" v-for="(comment, c_index) in post.comments" :key="c_index">
              <div class="border-top border-bottom">
                <span type='button' 
                  class=" border-bottom" 
                  @click="showUser(comment.c_userUsername)">
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
                <p> &emsp; {{ comment.comment }} </p>
              </div>
            </div>
          </div>
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


</template>

<script>
  import axios from "axios";
  import userStore from "../stores/counter.js";
  import dayjs from 'dayjs';
  import relativeTime from "dayjs/plugin/relativeTime";
  dayjs.extend(relativeTime);
  
export default {
  name: "BlogView",

  setup() {
    const store = userStore();
    return { store };
  },

  data() {
    return {
      posts: [],
      showingComments: '',
      editComId: "",
      update_comment: "",
      CPindex: "",
    };
  },

  methods: {
    // Required methods for the component
    showComments(index) {
      // this.showingComments = !this.showingComments;
      if(this.showingComments === index){
        this.showingComments = '';
      }else{
        this.showingComments = index;
      }
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
        post.newComment = '';
      }).catch(() => {
        alert("something went wrong, please try again")
      });
    },

    showUser(name){
      if(name !== this.store.userName){
        this.store.show_User(name);
        this.$router.push("/profile");
      }
    },

    like(blogId, index) {
      const headers = { 
        "Content-Type": "application/json",
        Authorization: "Bearer " + this.store.access_token,
      };

      axios.get(`http://localhost:5000/bloglite/blog/like/${blogId}`, { headers })
      .then((response) => {
        // console.log(response.data);
        // console.log(response.data.msg)
        // console.log(response.data.id)
        // console.log(this.posts[index].likes)
        if(response.data.id === 1){
          this.posts[index].likes += 1;
          this.posts[index].dislikes -= 1;
        }

        else if(response.data.id === 0){
          this.posts[index].likes += 1;
        }
      }).catch(() => {
        // console.log("something went wrong, please try again")
        alert("You have already liked this post")
      });
    },

    dislike(blogId, index) {
      const headers = { 
        "Content-Type": "application/json",
        Authorization: "Bearer " + this.store.access_token,
      };

      axios.get(`http://localhost:5000/bloglite/blog/dislike/${blogId}`, { headers })
      .then((response) => {

        if(response.data.id === 1){
          this.posts[index].dislikes += 1;
          this.posts[index].likes -= 1;
        }
        else if(response.data.id === 0){
          this.posts[index].dislikes += 1;
        }
      }).catch(() => {
        // console.log("something went wrong, please try again")
        alert("You have already liked this post")
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
    edit_Comment(event){
      event.preventDefault();
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
          // console.log(this.update_comment)
          this.posts[this.CPindex].comments[this.commentIndex].comment = this.update_comment
          this.posts[this.CPindex].comments.unshift(this.posts[this.CPindex].comments[this.commentIndex])
          this.posts[this.CPindex].comments.splice(this.commentIndex + 1, 1)
          alert(response.data.msg)
          this.commentIndex = '';
          this.editComId = '';
          this.update_comment = '';
        }).catch((error) => {
          // console.log(error)
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



  },
  computed: {
    // Computed properties for the component
    showCom() {
      return this.showingComments !== '';
    },
  },

// Lifecycle hooks for the component
  beforeMount() {
        if(!this.store.isLoggedIn){
          this.$router.push("/");
        }
  },

  mounted() {
    const headers = { 
        "Content-Type": "application/json",
        Authorization: "Bearer " + this.store.access_token,
      };
    
    axios.get('http://localhost:5000/bloglite/feed', { headers })
      .then((response) => {
        this.posts = response.data.feeds.blogs;
        // console.log(this.posts)
        this.posts.forEach((post) => {
                    post.blogCreation = dayjs(post.blogCreation).fromNow();
              });
      })
      .catch(() => {
        alert("something went wrong, please login again")
        // console.log(error);
      });
  },
} 
</script>
<style scoped>
.card-footer {
  /* margin-top: 10px;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f5f5f5; */
  max-height: 300px; /* set the maximum height of the comments container */
  overflow-y: auto; /* enable vertical scrolling when the content overflows */
}
</style>