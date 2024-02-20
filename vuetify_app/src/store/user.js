import { defineStore } from "pinia";

import { fetchWrapper } from "@/helpers/fetch-wrapper";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false,
    targetURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/users' : '/predictmod/users',
  }),

  actions: {
    async getCSRF() {
      // TODO: It would be better to not hit this API all the time...
      if (this.token !== null) {
        console.log("===> Already have CSRF: %s", this.token);
        return;
      };
      // console.log("---> Getting CSRF token");
      // console.log("---> Found MIDDLEWARE URL: %s", this.targetURL);
      const res = await fetchWrapper.get(`${this.targetURL}/csrf/`)
      const csrfToken = res['X-CSRFToken'];
      // console.log("---> Got CSRF Token: %s", csrfToken);
      this.token = csrfToken;
    },
    async login(email, password) {
      // console.log("---> Attempting to log in with credentials %s (%s)", email, password);
      // console.log("== CSRF Token is %s", this.token);
      const res = await fetch(`${this.targetURL}/login/`, {
        method: "POST",
        // credentials: "same-origin",
        credentials: "include",
        headers: {
          "Accept": 'application/json',
          // "Content-Type": "application/json",
          "X-CSRFToken": this.token,
        },
        body: JSON.stringify({ email, password }),
    });
      const user = await res.json();
      this.user = user['user'];
      console.log("===> Recieved user info: %s", JSON.stringify(user));
    },
    async logout() {
      // console.log('->>> Attempting to log out!');
      const res = await fetch(`${this.targetURL}/logout/`, {
        // method: "POST",  
        credentials: "include",
        // credentials: "same-origin",
        headers: {
          "Accept": 'application/json',
          // "Content-Type": "application/json",
          "X-CSRFToken": this.token,
        },
      })
      const response = await res.json();
      console.log("->>> Got response: %s", JSON.stringify(response));
    },
    async checkUser() {
      // console.log("---> Checking user @WhoAmI <---");
      console.log("=>>> User record: %s", this.user);
      const res = await fetch(`${this.targetURL}/whoami/`, {
        // credentials: "same-origin",
        credentials: "include",
        headers: {
          "Accept": "application/json",
          "X-CSRFToken": this.token,
        }
      })
      const response = await res.json();
      console.log("---> WhoAmI reported: %s", JSON.stringify(response));
    },
    async getSession() {
      console.log("---> Getting session <---");
      console.log("=>>> User record: %s", this.user);
      const res = await fetch(`${this.targetURL}/session/`, {
        // credentials: "same-origin",
        credentials: "include",
        headers: {
          "Accept": "application/json",
          "X-CSRFToken": this.token,
        },
      })
      const response = res.json();
      console.log("---> Got session info: %s", JSON.stringify(response));
    },
    showCSRFCookie() {
      console.log("->>> %s", JSON.stringify(this.token));
      console.log("->>> Current user? %s", JSON.stringify(this.user));
    },
    async createUser(email, password, firstName, lastName) {
      console.log("--> Attempting to register user with credentials:\nUser %s Password: %s\n Name: %s %s", email, password, firstName, lastName);
      const res = await fetch(`${this.targetURL}/create-user/`, {
        method: "POST",
        // credentials: "same-origin",
        // credentials: "include",
        // mode: "cross-origin",
        // headers: {
        //   "Accept": "application/json",
          // "csrfmiddlewaretoken": this.token,
        //   "X-CSRFToken": this.token,
        // },
        body: JSON.stringify(
          {
            "first_name": firstName,
            "last_name": lastName,
            "email": email,
            "password": password,
            // "csrfmiddlewaretoken": this.token,
          }
        )
      })
    }
  },
});
