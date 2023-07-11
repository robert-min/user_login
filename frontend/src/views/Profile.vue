<template>
    <div class="profile-page">
        <section class="section-profile-cover section-shaped my-0">
            <div class="shape shape-style-1 shape-primary shape-skew alpha-4">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
        </section>
        <section class="section section-skew">
            <div class="container">
                <card shadow class="card-profile mt--300" no-body>
                    <div class="px-4">
                        <div class="row justify-content-center">
                            <div class="col-lg-3 order-lg-2">
                                <div class="card-profile-image">
                                    <a href="#">
                                        <img v-lazy="'img/theme/minjun_char.jpeg'" class="rounded-circle">
                                    </a>
                                </div>
                            </div>
                            <div class="col-lg-4 order-lg-3 text-lg-right align-self-lg-center">
                                <div class="card-profile-actions py-4 mt-lg-0">
                                    <base-button type="info" size="sm" class="mr-4" @click="logOutUser">LogOut</base-button>
                                    <base-button type="default" size="sm" class="float-right" @click="deleteUser">Delete</base-button>
                                </div>
                            </div>
                            <div class="col-lg-4 order-lg-1">
                                <div class="card-profile-stats d-flex justify-content-center">
                                    <div>
                                        <span class="heading">22</span>
                                        <span class="description">Friends</span>
                                    </div>
                                    <div>
                                        <span class="heading">10</span>
                                        <span class="description">Photos</span>
                                    </div>
                                    <div>
                                        <span class="heading">89</span>
                                        <span class="description">Comments</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="text-center mt-5">
                            <h3>{{ respName }}
                                <span class="font-weight-light">, 27</span>
                            </h3>
                            <div class="h6 font-weight-300"><i class="ni location_pin mr-2"></i>{{ respEmail }}</div>
                            <div class="h6 mt-4"><i class="ni business_briefcase-24 mr-2"></i>Backend Engineer</div>
                            <div><i class="ni education_hat mr-2"></i>Hello!!</div>
                        </div>
                        <div class="mt-5 py-5 border-top text-center">
                            <div class="row justify-content-center">
                                <!-- <div class="col-lg-9">
                                    <p>An artist of considerable range, Ryan — the name taken by Melbourne-raised,
                                        Brooklyn-based Nick Murphy — writes, performs and records all of his own music,
                                        giving it a warm, intimate feel with a solid groove structure. An artist of
                                        considerable range.</p>
                                    <a href="#">Show more</a>
                                </div> -->
                            </div>
                        </div>
                    </div>
                </card>
            </div>
        </section>
    </div>
</template>
<script>
import axios from 'axios';
import router from "../router";
export default {
    name: "profile",
    data() {
    return {
      respEmail: "",
      respName: ""
    };
  },
    mounted() {
        // 로컬 스토리지에서 토큰 값 가져오기
        const token = localStorage.getItem('token');
        const email = localStorage.getItem('email');

        // 헤더에 토큰 값 설정
        axios.defaults.headers.common['Authorization'] = token;
        axios.defaults.headers.common['email'] = email;

        // 요청 보내기
        axios.get('http://15.165.197.195:8000/user/', { maxRedirects: 3 })
            .then(response => {
                // 요청이 성공한 경우
                if (response.status === 200) {
                    // 응답을 처리할 코드 작성
                    this.respEmail = response.data.result.email;
                    this.respName = response.data.result.name;
                }
            })
            .catch(error => {
                // 요청이 실패한 경우
                console.error(error);
            });
    },
    methods: {
        logOutUser(){
            // email 삭제
            localStorage.removeItem('email');

            // token 삭제
            localStorage.removeItem('token');
            router.push('/')
        },
        deleteUser() {
        // 로컬 스토리지에서 토큰 값 가져오기
        const token = localStorage.getItem('token');
        const email = localStorage.getItem('email');

        // 헤더에 토큰 값 설정
        axios.defaults.headers.common['Authorization'] = token;
        axios.defaults.headers.common['email'] = email;
        axios.delete('http://15.165.197.195:8000/user/')
            .then(response => {
                console.log(response);
                // 요청 성공 시 처리
                router.push('/');
            })
            .catch(error => {
            // 요청 실패 시 처리
            alert(error);
            });
    }
  }
};
</script>
<style></style>
