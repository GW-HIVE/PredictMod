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
        <h1>Clinician and Researcher Access</h1>
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
        <!-- <v-card> -->
          <v-card-title class="title text-center font-weight-bold">
            Login
          </v-card-title>

          <!-- <form @submit.prevent="login"> -->
          <!-- <form> -->
          <v-col>
            <v-row>
              <v-spacer></v-spacer>
              <v-text-field label="Email" v-model="email" style="width:50%"></v-text-field>
              <v-spacer></v-spacer>
              <!-- <input type="text" v-model="email" /> -->
            </v-row>
            <v-row>
              <v-spacer></v-spacer>
              <v-text-field label="Password" type="password" v-model="password" style="width:50%"></v-text-field>
              <v-spacer></v-spacer>
              <!-- <v-text-field label="Password" v-model="password"></v-text-field> -->
              <!-- <input type="password" v-model="password" /> -->
            </v-row>
            <v-row :v-if="loginError">
            <p style="color:#FF0000">
              {{ loginError }}
            </p>
          </v-row>
          <!-- </form> -->
        </v-col>
        <v-col>
          <v-row class="justify-center">
            <v-btn type="submit" @click.prevent="login()" :disabled="loggedIn">{{ loggedIn ? `${this.userStore.user}` : "Login"}}</v-btn>
            <v-btn type="submit" @click.prevent="logout()">Logout</v-btn>
          </v-row>
        </v-col>
        <!-- </v-card> -->
      </v-col>
      <v-col>
        <!-- <v-card class=""> -->
        <v-card-title class="title text-center font-weight-bold">
            Register
        </v-card-title>

        <!-- <form @submit.prevent="login"> -->
        <!-- <form> -->
          <v-col>
            <v-row>
            <v-spacer></v-spacer>
            <v-text-field label="First Name" v-model="firstName" style="width:40%"></v-text-field>
            <v-spacer></v-spacer>
            <v-text-field label="Last Name" v-model="lastName"  style="width:40%"></v-text-field>
            <v-spacer></v-spacer>
            </v-row>
            <v-row>
              <v-spacer></v-spacer>
            <v-text-field label="Email Address" v-model="newEmail" style="width:40%"></v-text-field>
              <v-spacer></v-spacer>
            <v-text-field label="Confirm Email" v-model="newEmailConfirmation" style="width:40%"></v-text-field>
              <v-spacer></v-spacer>
            </v-row>
          </v-col>
          <v-col>
            <v-row>
              <v-spacer></v-spacer>
              <v-text-field label="Password" type="password" v-model="newPassword" style="width:40%"></v-text-field>
              <v-spacer></v-spacer>
              <v-text-field label="Confirm Password" type="password" v-model="newPasswordConfirmation" style="width:40%"></v-text-field>
              <v-spacer></v-spacer>
            <!-- <input type="text" v-model="email" /> -->
          </v-row>
          </v-col>
          <v-row :v-if="userError" v-for="err in userError">
            <p style="color:#FF0000">
              {{ err }}
            </p>
          </v-row>
          <v-row class="justify-center">
            <v-btn type="submit" @click.prevent="createUser()">Create an Account</v-btn>
          </v-row>
        <!-- </form> -->
        <!-- </v-card> -->
      </v-col>
    </v-row>
  <v-spacer>
    <AdminDashboard v-if="showAdmin" />
  </v-spacer>
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

import AdminDashboard from '@/components/AdminDashboard.vue';
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
        firstName: "",
        lastName: "",
        newEmail: "",
        newEmailConfirmation: "",
        newPassword: "",
        newPasswordConfirmation: "",
        loginError: "",
        userError: [],
        loggedIn: false,
        showAdmin: false,
			}
    },
  mounted() {
    this.userStore.clearError();
    this.userStore.checkUser();
    if (this.userStore.isAdmin) {
      this.showAdmin = true;
    }
    if (this.userStore.user)  {
      this.loggedIn = true;
    }
  },
  components: { AdminDashboard, DisclaimerShow, LicenseShow },
  methods:
    {
      clearState() {
        this.email = "";
        this.password = "";
        this.newEmail = "";
        this.newEmailConfirmation = "",
        this.newPassword = "";
        this.newPasswordConfirmation = "",
        this.firstName = "";
        this.lastName = "",
        this.loginError = "";
        this.userError = [];
        this.userStore.clearError();
      },
      async login() {
        const success = await this.userStore.login(this.email, this.password);
        if (success) {
          console.log("Login confirmed ---> (Success was %s)", success);
          this.clearState();
          if (this.userStore.isAdmin) {
            this.showAdmin = true;
          }
          if (this.userStore.user !== "") {
            this.loggedIn = true;
          }
        } else {
          console.log("Error in login!");
          this.loginError = this.userStore.error;
          this.userStore.clearError();
        }
      },
      async logout() {
        const success = await this.userStore.logout();
        if (success) {
          this.userStore.clearError();
          this.showAdmin = false;
          this.loggedIn = false;
        } else {
          console.log("Error on logout!")
        }
      },

      async createUser() {
        this.userError = [];
        console.log(
          "New Email: %s\nConfirmation: %s\nNPass: %s\nConfirm Pass: %s",
          this.newEmail,
          this.newEmailConfirmation,
          this.newPassword,
          this.newPasswordConfirmation
        );
        console.log("Bools: %s // %s", 
        this.newEmail != this.newEmailConfirmation,
        this.newPassword != this.newPasswordConfirmation
        )

        if (this.newEmail != this.newEmailConfirmation) {
          this.userError.push("New email doesn't match");
        }
        if (this.newPassword != this.newPasswordConfirmation) {
          this.userError.push("\nNew passwords don't match\n");
        }
        if (this.userError.length > 0) {
          return;
        }
        const success = await this.userStore.createUser(
          this.newEmail, this.newPassword, this.firstName, this.lastName
        );
        if (success) {
          this.clearState();
          if (this.userStore.isAdmin) {
            this.showAdmin = true;
          }
          if (this.userStore.user !== "") {
            this.loggedIn = true;
          }
          return;
        } else {
          console.log("Error - Handling error on unsuccessful creation");
          this.userError.push(this.userStore.error);
          this.userStore.clearError();
        }
      },

    }
}
</script>
