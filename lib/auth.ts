import { 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  User
} from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { auth, db } from './firebase';
import type { UserProfile } from './content';

export async function signUp(email: string, password: string, name: string) {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  const user = userCredential.user;

  const userProfile: UserProfile = {
    id: user.uid,
    name: name,
    plan: 'free',
    xp: 0,
    badges: [],
    streakDays: 0,
    completedLessons: [],
    currentCourseId: 'ai-coding',
    currentLessonId: 'ai01'
  };

  await setDoc(doc(db, 'users', user.uid), userProfile);
  
  return { user, userProfile };
}

export async function signIn(email: string, password: string) {
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  return userCredential.user;
}

export async function signOut() {
  await firebaseSignOut(auth);
}

export async function getUserProfile(userId: string): Promise<UserProfile | null> {
  const docRef = doc(db, 'users', userId);
  const docSnap = await getDoc(docRef);
  
  if (docSnap.exists()) {
    return docSnap.data() as UserProfile;
  }
  
  return null;
}

export async function updateUserProgress(
  userId: string, 
  updates: Partial<UserProfile>
) {
  const docRef = doc(db, 'users', userId);
  await setDoc(docRef, updates, { merge: true });
}

export function onAuthChanged(callback: (user: User | null) => void) {
  return onAuthStateChanged(auth, callback);
}
