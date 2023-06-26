// import { ref, computed } from "vue";
import axios from "axios";
import { defineStore } from "pinia";


// get cookie for token
function get_cookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
// delete cookie
function delete_cookie(name) {
  if (get_cookie(name)) {
    document.cookie = name + "=" + ";expires=Thu, 01 Jan 1970 00:00:01 GMT";
  }
}


export const userStore = defineStore("counter", {


  state: () => ({
    token: get_cookie("access_token"),
    userData: {
      userId: "",
      name: "",
      userName: "",
      userImg: "",
      userNoPost: "",
      userNoFollowers: "",
      userNoFollowing: "",
    },


    searchUser: {
      searchUsername: "",
    },


    

  }),

  getters: {
    access_token: (state) => state.token, 
    isLoggedIn: (state) => state.token !== "",
    userName: (state) => state.userData.userName,
    noblogs: (state) => state.userData.userNoPost,
    searchUsername: (state) => state.searchUser.searchUsername,

    name: (state) => state.userData.name,
    new_blog_creation: (state) => state.new_blog_creation,

  },

  actions: {
    // get user data
    async getUser() {
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + document.cookie.split("=")[1],
      };
      
      const response = await axios.get("http://localhost:5000/bloglite/user",  { headers });
      if (response.status === 200) {
        // console.log(response)
        this.setUser(response.data.user);
        // console.log(response.data.user);
      } else {
        // const error = await response.json();
        this.errorMsg = error.error;
        console.log(error.error)
      }

    },
    // search Userdata
    // set user data
    setUser(user) {
      this.userData.userId = user.userId;
      this.userData.name = user.userName;
      this.userData.userName = user.userUsername;
      this.userData.userImg = user.userImgUrl;
      this.userData.userNoPost = user.userNoBlog;
      this.userData.userNoFollowers = user.userNoFollowers;
      this.userData.userNoFollowing = user.userNoFollowing;
    },


    setToken(access_token){
      this.token = access_token;
      document.cookie = "";
    },

    c_logout() {

      this.token = "";
      delete_cookie("access_token"); 
      // console.log("deleteing_cookie")
      // console.log(get_cookie("access_token")) 
      document.cookie = "";
      // console.log(document.cookie)
      // console.log(this.token)
      // console.log(this.isLoggedIn)

    },


    show_User(user) {
      this.searchUser.searchUsername = user;
      // console.log(this.searchUser.searchUsername)
    },

    new_blog_(){     
      this.userData.userNoPost += 1
      // console.log("updated the post value")
    },
    

    
    delete_blog(){
      this.userData.userNoPost -= 1
      console.log("deleted the post value")
    }

    
  },
}); // <--- this is the store




export default userStore;