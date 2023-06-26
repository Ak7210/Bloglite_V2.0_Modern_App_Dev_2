<template>
    <!-- Modal -->
    <div class="modal fade" id="updateBlog" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="staticBackdropLabel">Update Blog</h1>
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
                <!-- <input type="text" class="form-control" rows="5" v-model="content" required>
                 -->
                 <textarea class="form-control" id="updatedcontent" rows="3" v-model="content"></textarea>
              </div>
  
              <div class="mb-3" >
                <input type="file"  ref="file" @change="uploadFile">
                <button type="button" class="btn btn-success btn-sm" @click="submitFile">Upload</button>
                <!-- <button @click="onUpload">Upload</button> -->
              </div>


              <div class="form-check">
                <div >
                  <input class="form-check-input" type="checkbox" id="remove" v-model="isRemove">
                  <label class="form-check-label" for="remove">remove image</label>
                </div>               


                <div>
                  <input class="form-check-input" type="radio" name="exampleRadios" id="private" value="private" v-model="selectedOption">
                  <label class="form-check-label" for="private">
                    Private
                  </label>
                </div>
                  <div>
                    <input class="form-check-input" type="radio" name="exampleRadios" id="public" value="public" v-model="selectedOption">
                    <label class="form-check-label" for="public">
                      Public
                    </label>
                  </div>

              </div>  
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="createBlog">Update</button>
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
  
  export default {

    name: 'editBlog',
    // Props that will be passed to this component from the parent component (ProfileComp.vue) 
    props: ['editBlogId'],
    emits: ['updatedBlog'],

    data() {
      return {
        blogTitle: '',
        content: "",
        imageUrl: "",
        isRemove: false,
        deleteImg: false,
        selectedOption: null,
        edit_blog_id: "", 
        Images: null,       
      };
    },
    
    setup() {
      const store = userStore();
      return { store };
    },

    methods: {
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
          .then((response) => {
            const data = response.data;
            // console.log(response.data.msg);
            // console.log(data.imageUrl)
            this.imageUrl = response.data.imageUrl;
            alert(response.data.msg);
            // console.log(response.data);
  
            // handle successful response
          })
          .catch(error => {
            alert("Something went wrong");
            // console.log(error);
            // handle error
          });
      },
  
  
      async createBlog(event) {
        // Prevent the default form submit event
        console.log(this.editBlogId)
        // console.log(this.blogId)
        if(this.store.u_blogId != '') {
          this.edit_blog_id = this.store.u_blogId;
        }
        event.preventDefault();
        // Create a FormData object
          const data=  JSON.stringify({
            "blogTitle": this.blogTitle,
            "caption": this.content,
            "imageUrl": this.imageUrl,
            "isArchived": this.selectedOption,
            "deleteImg": this.isRemove,
          });
  
        // send the data to the server
  
        const headers = { 
          "Content-Type": "application/json",
          Authorization: "Bearer " + this.store.access_token, };
          
        const response = await axios.put(`http://localhost:5000/bloglite/blog/${this.editBlogId}`, data, { headers });

  
        // const new_data = await response.json();
        if (response.status === 200) {
          console.log(response.data.updateblog)
          // this.store.updateBlog(response.data.updateblog)
          this.$emit('updatedBlog', response.data.updateblog);
          // remove all the data after update the blog
          this.blogTitle = "";
          this.content = "";
          this.imageUrl = "";
          this.isRemove = false;
          this.selectedOption = null;
          this.deleteImg = false;
          this.Images = null;  
          alert('Blog updated successfully! Please refresh the page to see the changes');
        } else {
          // this.username_errorMsg = data.message;
          // console.log(new_data);
          alert(response.data.msg);
        }
      },
    },
  };
  </script>
  
  
  
  
  
