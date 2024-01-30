import { useState } from "react";
import "./App.css";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import { getUser } from "./firebase";
import { NewUser } from "./NewUser";
import { ExistingUser } from "./ExistingUser";

function App() {
  const [userEmail, setUserEmail] = useState("");
  const [userData, setUserData] = useState(null);
  if (userEmail === "") {
    return (
      <GoogleOAuthProvider clientId="588906453007-7j6lcdngva3rsuhm37qdjeq515kavjvl.apps.googleusercontent.com">
        <GoogleLogin
          onSuccess={(credentialResponse) => {
            console.log(credentialResponse);
            var decoded = jwtDecode(credentialResponse.credential);
            console.log(decoded);
            // localStorage.setItem("userEmail", decoded.email);
            setUserEmail(decoded.email);
          }}
          onError={() => {
            console.log("Login Failed");
          }}
        />
      </GoogleOAuthProvider>
    );
  } else {
    getUser(userEmail).then((data) => {
      setUserData(data);
    });

    if (userData === null) {
      return <NewUser />;
    } else {
      return <ExistingUser userData={userData} />;
    }
  }
}

export default App;
