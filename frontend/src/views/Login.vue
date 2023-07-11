<template>
    <section class="section section-shaped section-lg my-0">
        <div class="shape shape-style-1 bg-gradient-default">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
        </div>
        <div class="container pt-lg-md">
            <div class="row justify-content-center">
                <div class="col-lg-5">
                    <card type="secondary" shadow
                          header-classes="bg-white pb-5"
                          body-classes="px-lg-5 py-lg-5"
                          class="border-0">
                        <!-- <template>
                            <div class="text-muted text-center mb-3">
                                <small>Sign in with</small>
                            </div>
                            <div class="btn-wrapper text-center">
                                <base-button type="neutral">
                                    <img slot="icon" src="img/icons/common/github.svg">
                                    Github
                                </base-button>

                                <base-button type="neutral">
                                    <img slot="icon" src="img/icons/common/google.svg">
                                    Google
                                </base-button>
                            </div>
                        </template> -->
                        <template>
                            <div class="text-center text-muted mb-4">
                                Login Service
                            </div>
                            <form role="form">
                                <base-input alternative
                                            class="mb-3"
                                            placeholder="Email"
                                            addon-left-icon="ni ni-email-83"
                                            v-model="email">
                                </base-input>
                                <base-input alternative
                                            type="password"
                                            placeholder="Password"
                                            addon-left-icon="ni ni-lock-circle-open"
                                            v-model="password">
                                </base-input>
                                <!-- <base-checkbox>
                                    Remember me
                                </base-checkbox> -->
                                <div class="text-center">
                                    <base-button type="primary" class="my-4" @click="submitForm">Log In</base-button>
                                </div>
                            </form>
                        </template>
                    </card>
                    <div class="row mt-3">
                        <div class="col-6">
                            <a href="#" class="text-light">
                                <small></small>
                            </a>
                        </div>
                        <div class="col-6 text-right">
                            <a href="#" class="text-light">
                                <router-link to="/register" class="text-light">Create new account</router-link>
                                
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
<script>
import axios from "axios";
import BaseInput from "../components/BaseInput.vue"
import router from "../router"
export default {
    name: "login",
    components: {
        BaseInput
    },
    data() {
    return {
      email: '',
      password: ''
    };
  },
    methods: {
    submitForm() {
      // email 값을 서버로 요청
      axios.post('http://localhost:8000/auth/login', { email: this.email, password: this.password })
        .then(response => {
          // 요청 성공 시 처리
          console.log(response.data.result.email);
          localStorage.setItem('token',response.data.result.token)
          localStorage.setItem('email',response.data.result.email)
          router.push('/profile')
        })
        .catch(error => {
          // 요청 실패 시 처리
          alert(error.response.data.message);
        });
    }
  }
  };
  
</script>
<style>
</style>
