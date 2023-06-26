<template>
  <div class="modal fade" id="createBlog" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="staticBackdropLabel">Create Blog</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          
          <form class="form" role="form" autocomplete="off" >
            <div class="mb-3 mt-2">
              <label for="blogTitle" class="form-label">Blog Title</label>
              <input type="text" class="form-control" v-model="blogTitle" required>
            </div>

            <div class="mb-3">
              <label for="comment" class="form-label">Blog Caption</label>
               <textarea class="form-control" id="content" rows="3" v-model="content"></textarea>
            </div>

            <div class="mb-3" >
              <input type="file"  ref="file" @change="uploadFile">
              <button type="button" class="btn btn-success btn-sm" @click="submitFile" v-if="Images!= null && blogTitle!=''">Upload</button>

            </div>

            <div class="form-check mb-3">
                <input class="form-check-input" type="checkbox" id="archive" v-model="isArchived">
                <label class="form-check-label" for="archive">Blog Archive</label>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="createBlog" v-if="blogTitle!=''">Create</button>
            </div>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
import userStore from "../stores/counter.js";
import dayjs from 'dayjs';
import relativeTime from "dayjs/plugin/relativeTime";
dayjs.extend(relativeTime);

export default {
  name: 'BlogCreate',
  emits: ['new_blog'],
  
  data() {
    return {
      blogTitle: '',
      content: "",
      imageUrl: "",
      Images: null,
      isArchived: false,
    };
  },

  setup() {
    const store = userStore();
    return { store };
  },

  methods: {
    // Required methods for the component
    fileUpload() {
      this.file = this.$refs.file.files[0];
    },

    uploadFile(event) {
      event.preventDefault();
      this.Images = this.$refs.file.files[0];
    },
    submitFile(event) {
      event.preventDefault();
      const formData = new FormData();
      formData.append('files', this.Images);

      const headers = { 
        'Content-Type': 'multipart/form-data',
        Authorization: "Bearer " + this.store.access_token,
       };
      axios.post('http://127.0.0.1:5000/bloglite/blog/image', formData, { headers })
        .then(response => {
          // console.log(response.data.msg);
          this.imageUrl = response.data.imageUrl;
          alert(response.data.msg);
          // console.log(response.data);
        })
        .catch(() =>{
          // console.log(error);
          alert("something went wrong please try again")
        });
    },


    async createBlog(event) {
      // Prevent the default form submit event
      event.preventDefault();
      // Create a FormData object
        const data=  JSON.stringify({
          "blogTitle": this.blogTitle,
          "caption": this.content,
          "imageUrl": this.imageUrl,
          "isArchived": this.isArchived,
        });

      // send the data to the server

      const headers = { 
        "Content-Type": "application/json",
        Authorization: "Bearer " + this.store.access_token
      };
      axios.post("http://localhost:5000/bloglite/blog", data, { headers })
        .then(response => {
          console.log(response.data)
          alert(response.data.msg);
          this.store.new_blog_();
          response.data.blog.blogCreation = dayjs(response.data.blog.blogCreation).fromNow();

          this.$emit("new_blog", response.data.blog)
          
          // clear the form after submission
          this.blogTitle = "";
          this.content = "";
          this.imageUrl = "";
          this.Images = null;
          this.isArchived = false;
        })
        .catch(() =>{
          // console.log(error);
          alert("something went wrong please try again")
        });

      },
  },
};
</script>