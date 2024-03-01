import { defineStore } from "pinia";

import { getCookie } from "@/helpers/cookies";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
    token: null,
    isAdmin: false,
    isAuthenticated: false,
    error: null,
    targetURL: import.meta.env.DEV ? import.meta.env.VITE_DEV_MIDDLEWARE_BASE + '/api' : '/predictmod/api',
  }),

  mounted() {
    // Update the CSRF token when the store has been remounted
    //  (eg, the page has been refreshed)
    this.checkUser();
  },
  actions: {

    clearError() {
      this.error = null;
    },

    handleUserResponse(response) {
      console.log("Handling response: %s", JSON.stringify(response));
      if (response.error) {
        this.error = response.error;
        return false;
      }

      if (response.detail) {
        this.error = response.detail;
        return false;
      }

      if (response.created || response.update) {
        console.log("Found a user creation / update");
        // No updates, but operation was successful
        return true;
      };
      
      if (response.admin) {
        console.log("Confirming admin access ....");
        this.isAdmin = true;
      } else {
        this.isAdmin = false
      };

      if (!response.username) {
        console.log("Got a response username: %s", response.username);
        this.user = null;
        this.token = null;
        return false;
      }
      this.user = response['username'];
      this.token = getCookie('csrftoken');
      return true;
    },

    async login(email, password) {
      const res = await fetch(`${this.targetURL}/login/`, {
        method: "POST",
        // credentials: "same-origin",
        credentials: "include",
        headers: {
          "Accept": 'application/json',
          // "Content-Type": "application/json",
          // "X-CSRFToken": this.token,
        },
        body: JSON.stringify({ email, password }),
      });
    
      if (!res.ok) {
        // Error handling
      }

      const response = await res.json();

      if (!response){
        // Error handling
      }

      const success = this.handleUserResponse(response);
      if (!success) {
        console.log("Error on login - response was %s", JSON.stringify(response));
      }
      return success;
    },

    async logout() {
      // console.log('->>> Attempting to log out!');
      // const response = this.fetchHelper("/logout", true);
      if (!this.user && !this.token) {
        this.user = null; 
        this.token = null;
        return true;
      }
      const res = await fetch(`${this.targetURL}/logout/`, {
        // method: "POST",  
        credentials: "include",
        // credentials: "same-origin",
        headers: {
          "Accept": 'application/json',
          // "Content-Type": "application/json",
          // "X-CSRFToken": this.token,
        },
      })
      if (!res.ok) {
        // Error handling
      }

      const response = await res.json();
      var success = this.handleUserResponse(response);
      // success should be false on logout
      success = !success;
      if (!success) {
        console.log("Error in logout - see logs")
      }
      this.user = null;
      this.token = null;
      this.isAdmin = false;

      console.log("User store state is now: User %s Token %s", this.user, this.token);

      return success;
    },

    async checkUser() {
      console.log("=>>> User record: %s", this.user);
      const res = await fetch(`${this.targetURL}/whoami/`, {
        // credentials: "same-origin",
        credentials: "include",
        headers: {
          "Accept": "application/json",
          // "X-CSRFToken": this.token,
        }
      })
      if (!res.ok) {
        /// Error handling
      }
      const response = await res.json();

      // console.log("---> WhoAmI reported: %s", JSON.stringify(response));
      
      const success = this.handleUserResponse(response);
      if (!success){
        // Error handling. NB: Users not yet logged in will
        // return `false`y from handleUserResponse.
        // console.log("Error on checking user through `whoami`");
      }

      return success;

    },

    async createUser(email, password, firstName, lastName) {
      console.log("--> Attempting to register user with credentials:\nUser %s Password: %s\n Name: %s %s", email, password, firstName, lastName);

      const res = await fetch(`${this.targetURL}/create-user/`, {
        method: "POST",
        // credentials: "same-origin",
        // credentials: "include",
        // mode: "cross-origin",
        headers: {
          "Accept": "application/json",
          // "X-CSRFToken": this.token,
        },
        body: JSON.stringify(
          {
            "first_name": firstName,
            "last_name": lastName,
            "email": email,
            "password": password,
          }
        )
      })

      if (!res.ok) {
        // Error handling
      }

      const response = await res.json();

      const success = this.handleUserResponse(response);
      if (!success) {
        console.log("Error on user creation - See logs");
      }
      return success;
    },

    async updateProfile(userID, firstName, lastName, password, email) {
    console.log("Current CSRF token: %s", this.token);
    const res = await fetch(`${this.targetURL}/update-user/`, {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": this.token,
      },
      body: JSON.stringify({
        "first_name": firstName,
        "last_name": lastName,
        "password": password,
        "email": email,
        "user_id": userID,
      })
    })

    if (!res.ok) {
      // Error handling
    }
    const response = await res.json();
    const success = this.handleUserResponse(response);
    if (!success) {
      // Error handling
    }
    return success;
  },

  async updatePassword(userID, oldPassword, newPassword) {
    this.error = null;
    const res = await fetch(`${this.targetURL}/update-user/`, {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": this.token,
      },
      body: JSON.stringify({
        "old_password": oldPassword,
        "new_password": newPassword,
        "user_id": userID,
      })
    })

    if (!res.ok) {
      // Error handling
    }

    const response = await res.json();

    const success = this.handleUserResponse(response);
    if (!success) {
      // Error handling
    }
    return success;
  },

  async deleteUser(userID) {
    this.error = null;
    const res = await fetch(`${this.targetURL}/delete-user/`, {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": this.token,
      },
      body: JSON.stringify({
        "user_id": userID,
      })
    })

    if (!res.ok) {
      // Error handling
      console.log("User deletion: Result not OK!");
    }

    const response = await res.json();

    var success = this.handleUserResponse(response);
    // success should be false on deletion
    success = !success;
    if (!success) {
      // Error handling
    }
    console.log("User store: Deletion final report: %s", success);
    return success;
  },
  }
});
