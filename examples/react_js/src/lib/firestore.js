import { initializeApp } from "firebase/app";
import {
  getAuth,
  signInWithEmailAndPassword,
} from "firebase/auth";
import { getFirestore, collection, addDoc } from "firebase/firestore";

const firebaseConfig = {
    apiKey: "AIzaSyB6WPIVzMaRCnlL1ZmRosrQsbQYYagZARQ",
    authDomain: "trubrics-streamlit.firebaseapp.com",
    projectId: "trubrics-streamlit",
  };

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export const init = (email, password) => {
    signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        console.log(userCredential.user.email, "signed in!!")
    })
    .catch((error) => {
        window.alert(error.message);
    });
}

export const save = async (email, score, text, componentName) => {
  const date = new Date()
  addDoc(
      collection(db, "organisations", email, "feedback", componentName, "responses"),
      {
        component_name: componentName,
        model: "test",
        response: {
          type: "thumbs",
          score: score,
          text: text,
        },
        created_on: date,
        user_id: null,
        tags: ["react"],
        metadata: {},
      },
  );
};
