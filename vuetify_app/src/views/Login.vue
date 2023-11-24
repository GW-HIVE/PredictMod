<template>
  <v-banner
  single-line
  class="text-left">
    <v-img
      src="../assets/Welcome_Header.jpg"
      id="intro-img"
      gradient="to bottom, rgba(119, 119, 119, 0.25), rgba(0, 0, 0, 0.75)"
      :height="400" 
      :cover="true"
      >
      <div class="d-flex fill-height" style="flex-direction:column">
          <div class="d-flex fill-height align-center justify-center"> 
            <v-card flat color="transparent">
      <v-card-title class="title text-center font-weight-bold">
        Clinician and Researcher Access
      </v-card-title>
      </v-card>
      </div>
      </div>
      <!-- <span class="introduction">PredictMod Test Text</span> -->
    </v-img>
  </v-banner>

  <v-container>


    <v-row class="justify-center">
      <v-col>

        <v-card-title class="title text-center font-weight-bold">
          Login or register for access to PredictMod          
        </v-card-title>

        <!-- <form @submit.prevent="login"> -->
        <form>
          <v-row>
            <v-text-field label="Email" v-model="email"></v-text-field>
            <!-- <input type="text" v-model="email" /> -->
          </v-row>
          <v-row>
            <v-text-field label="Password" type="password" v-model="password"></v-text-field>
            <!-- <v-text-field label="Password" v-model="password"></v-text-field> -->
            <!-- <input type="password" v-model="password" /> -->
          </v-row>
          <v-row>
          <v-btn type="submit" @click.prevent="login()">Login</v-btn>
          <v-btn type="submit" @click.prevent="logout()">Logout</v-btn>
          <v-btn type="submit" @click.prevent="checkUser()">Who Am I?!</v-btn>
          <v-btn type="submit" @click.prevent="getSession()">Session info</v-btn>
          <v-btn type="submit" @click.prevent="showCSRFCookie()">Show CSRF Token</v-btn>
          <!-- <v-btn type="submit" @click.prevent="tbdAlert()">Register</v-btn> -->
        </v-row>
        </form>

      </v-col>
    
    </v-row>
<!-- 
    <v-container>
    <v-row class="justify-center">
      <v-card-title class="title text-center font-weight-bold" >
        <v-btn @click.prevent="tbdAlert()">
          Login
          // Original comment: Unclear if this is needed in v-btn: href="/predictmod/admin/login/"
        </v-btn>
        <v-btn @click.prevent="tbdAlert()">
          // Original comment: Unclear if this is needed in v-btn: href="/predictmod/admin/register/"
          Register
        </v-btn>
      </v-card-title>
    </v-row>
    </v-container>
     -->
    <v-row>
      <v-col>
        <DisclaimerShow/>
      </v-col>
      <v-col>
        <LicenseShow/>
      </v-col>
    </v-row>


</v-container>

<!-- <v-img src="../assets/Footer.png">
  
</v-img> -->


</template>
<script>
import { onMounted, ref } from 'vue';

import DisclaimerShow from './DisclaimerShow.vue';
import NotFound from './NotFound.vue';
import LicenseShow from './LicenseShow.vue';

import { useUserStore } from '@/store/user';

export default {

  name: 'Home',
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  data() {
			return {
				home: false,
        email: "",
        password: "",
			}
    },
  mounted() {
    this.resolveTargetURL();
    this.getCSRF();
  },
  components: { DisclaimerShow, LicenseShow },
  methods:
    {
      resolveTargetURL() {
        this.userStore.resolveMiddleware();
      },
      getCSRF() {
        this.userStore.getCSRF();
      },
      login() {
        this.userStore.login(this.email, this.password);
      },
      logout() {
        this.userStore.logout();
      },
      checkUser() {
        this.userStore.checkUser();
      },
      getSession() {
        this.userStore.getSession();
      },
      showCSRFCookie() {
        this.userStore.showCSRFCookie();
      }
    }
}
</script>
