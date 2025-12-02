import { 
  collection, 
  doc, 
  getDoc, 
  getDocs, 
  query, 
  where,
  setDoc,
  updateDoc,
  arrayUnion
} from 'firebase/firestore';
import { db } from './firebase';
import type { CourseDefinition, LessonDefinition, UserProfile } from './content';

export async function getCourse(courseId: string): Promise<CourseDefinition | null> {
  const docRef = doc(db, 'courses', courseId);
  const docSnap = await getDoc(docRef);
  
  if (docSnap.exists()) {
    return docSnap.data() as CourseDefinition;
  }
  
  return null;
}

export async function getAllCourses(): Promise<CourseDefinition[]> {
  const coursesRef = collection(db, 'courses');
  const snapshot = await getDocs(coursesRef);
  
  return snapshot.docs.map(doc => doc.data() as CourseDefinition);
}

export async function getLesson(lessonId: string): Promise<LessonDefinition | null> {
  const docRef = doc(db, 'lessons', lessonId);
  const docSnap = await getDoc(docRef);
  
  if (docSnap.exists()) {
    return docSnap.data() as LessonDefinition;
  }
  
  return null;
}

export async function getLessonsByChapter(chapterId: string): Promise<LessonDefinition[]> {
  const lessonsRef = collection(db, 'lessons');
  const q = query(lessonsRef, where('chapterId', '==', chapterId));
  const snapshot = await getDocs(q);
  
  return snapshot.docs.map(doc => doc.data() as LessonDefinition);
}

export async function completeLesson(userId: string, lessonId: string, xpGained: number) {
  const userRef = doc(db, 'users', userId);
  
  await updateDoc(userRef, {
    completedLessons: arrayUnion(lessonId),
    xp: xpGained,
    currentLessonId: lessonId
  });
}

export async function updateUserCourse(userId: string, courseId: string, lessonId: string) {
  const userRef = doc(db, 'users', userId);
  
  await updateDoc(userRef, {
    currentCourseId: courseId,
    currentLessonId: lessonId
  });
}

export async function addBadge(userId: string, badgeName: string) {
  const userRef = doc(db, 'users', userId);
  
  await updateDoc(userRef, {
    badges: arrayUnion(badgeName)
  });
}
