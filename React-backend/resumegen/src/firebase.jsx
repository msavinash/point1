import { initializeApp } from "firebase/app";
import {
  getFirestore,
  collection,
  getDocs,
  getDoc,
  doc,
} from "firebase/firestore/lite";

const firebaseConfig = {
  apiKey: "AIzaSyDaYmywe8zwYYfLmrD3k3YjCDjvY7RlJJg",
  authDomain: "tailores-01.firebaseapp.com",
  projectId: "tailores-01",
  storageBucket: "tailores-01.appspot.com",
  messagingSenderId: "1060330181597",
  appId: "1:1060330181597:web:218cf40836c680a3521c34",
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function getUser(userEmail) {
  const resumeDataRef = doc(db, "resume-data", userEmail);
  const resumeDataSnap = await getDoc(resumeDataRef);
  if (resumeDataSnap.exists()) {
    return resumeDataSnap.data();
  } else {
    return null;
  }
}

export { getUser };
