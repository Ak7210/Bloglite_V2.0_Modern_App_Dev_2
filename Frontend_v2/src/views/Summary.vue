<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-8">
                <apexchart id="summaryChart"  type="bar" :options="options" :series="series" height="600" width="100%" style="margin-top:2%; margin-left:6%"></apexchart>
            </div>
            <div class="col-md-4" >
                <div style="margin-left:30%; margin-top: 15%;">
                    <p style="font-family: cursive;">Number of Followers: {{ this.followers }}</p>
                    <p style="font-family: cursive;">Number of Followings: {{ this.following }}</p>
                    <p style="font-family: cursive;">Number of Blogs: {{ this.blogs }}</p>
                    <p style="font-family: cursive;">Comments posted by you: {{ this.comments }}</p>                    
                </div>
                <div class="d-flex position-relative-reverse">
                <button type="button" 
                class="btn btn-dark btn-sm position-absolute position-absolute top-0 end-0"
                style="margin-top: 2%; margin-right: 1%;"
                @click="home()">Go to home page</button>
        </div><br> 
            </div>
        </div>
    
    </div>
</template>

<script>

import userStore from '../stores/counter';
import axios from 'axios';

export default {
    name: "Summary",
    data() {
        return {
            options: {
                chart: {
                    id: 'summaryChart'
                },
                title: {
                    text: "Summary of your blogs",
                    align: 'center',
                    style: {
                        fontSize: '20px',
                        // fontWeight: 'bold'
                        fontFamily: 'cursive',
                    }

                },
                legend: {
                    position: "top",
                    horizontalAlign: "center",
                    offsetY: -10,
                    },
                xaxis: {
                    categories: [],
                    labels: {
                        offsetY: -2,
                        style: {
                            fontSize: '10px',
                            // fontWeight: 'bold'
                        }
                    },
                    title: {
                        text: 'Blog Title',
                        style: {
                            fontSize: '15px',
                            fontWeight: 'bold'
                            
                        }
                    }
                },
                yaxis: {
                    title: {
                        text: '#Likes/dislikes/comments',
                        style: {
                            fontSize: '15px',
                            fontWeight: 'bold'
                        }
                    }
                },
                dataLabels: {
                    enabled: true,
                    offsetX: -6,
                    style: {
                        fontSize: '12px',
                        colors: ['#fff']
                        }
                },
                plotOptions: {
                    bar: {
                        horizontal: false,
                        columnWidth: '40%',
                        endingShape: 'rounded'
                    },
                },


            },
            series: [
                {

                    name: 'Number of comments',
                    data: []
                },
                {
                    name: 'Number of likes',
                    data: []
                },
                {
                    name: 'Number of dislikes',
                    data: []
                }
            ],
            followers: 0,
            following: 0,
            blogs: 0,
            comments: 0,
        };

        
    },

    setup() {
        const store = userStore();
        return { store };
    },
    methods: {
        home() {
            this.$router.push({ name: 'Home Page' });
        }
    },

    // lifecycle hooks
    mounted() {
        const headers = {
            'Content-Type': 'application/json',
            Authorization: "Bearer " + this.store.access_token, 
        };
        axios.get("http://localhost:5000/bloglite/summary", { headers })
        .then((response) => {
            console.log(response.data);
            console.log(response.data.comment_on_blogs)
            if(response.data.comment_on_blogs.length == 0) {
                this.options.xaxis.categories.push("No Blogs found");
                this.series[0].data.push(0);
            }
            else{
                for(let i = 0; i < response.data.comment_on_blogs.length; i++) {
                    this.options.xaxis.categories.push(response.data.comment_on_blogs[i][0]);
                    this.series[0].data.push(response.data.comment_on_blogs[i][1]);
                    this.series[1].data.push(response.data.comment_on_blogs[i][2]);
                    this.series[2].data.push(response.data.comment_on_blogs[i][3]);
                }
            }
            this.followers = response.data.number_of_followers;
            this.following = response.data.number_of_followings;
            this.blogs = response.data.number_blogs_created;
            this.comments = response.data.users_comment;
            // console.log(this.options.xaxis.categories);
            // console.log(this.series[0].data);
            // console.log(this.series[1].data);
            // console.log(this.series[2].data);

            // this.store.summary = response.data;
        }).catch(() => {
            // console.log("error");
            alert("Error in fetching summary data")
        });
    },

}
</script>
<style scoped>
.wrapper {
  display: flex;
}

.chart-container {
  flex: 1;
}

.info-container {
  flex: 1;
}
</style>