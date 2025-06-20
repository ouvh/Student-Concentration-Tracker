import os
import shutil
import chromadb

def reset_face_tracking_database():
    """Reset the face tracking database by removing all data"""
    db_path = "./face_vectors_db"
    
    try:
        # Try to delete the collection first using ChromaDB API
        try:
            client = chromadb.PersistentClient(path=db_path)
            try:
                client.delete_collection("face_encodings")
                print("Successfully deleted face_encodings collection")
            except:
                print("No collection to delete or error deleting collection")
        except Exception as e:
            print(f"Error accessing ChromaDB: {e}")
        
        # Delete the directory if it exists
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            print(f"Removed directory: {db_path}")
        
        print("Face tracking database has been reset. The application will create a new database on next startup.")
    except Exception as e:
        print(f"Error resetting database: {e}")

if __name__ == "__main__":
    reset_face_tracking_database()
