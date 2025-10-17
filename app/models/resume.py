from typing import Dict, List
import uuid


class ResumeModel:
    """In-memory storage for resumes (replace with database in production)."""
    
    def __init__(self):
        self._storage: Dict[str, dict] = {}
    
    def create(self, resume_data: dict) -> dict:
        """Create a new resume."""
        resume_id = str(uuid.uuid4())
        resume_data["id"] = resume_id
        self._storage[resume_id] = resume_data
        return resume_data
    
    def get(self, resume_id: str) -> dict:
        """Get a resume by ID."""
        return self._storage.get(resume_id)
    
    def get_all(self) -> List[dict]:
        """Get all resumes."""
        return list(self._storage.values())
    
    def update(self, resume_id: str, resume_data: dict) -> dict:
        """Update a resume."""
        if resume_id in self._storage:
            resume_data["id"] = resume_id
            self._storage[resume_id] = resume_data
            return resume_data
        return None
    
    def delete(self, resume_id: str) -> bool:
        """Delete a resume."""
        if resume_id in self._storage:
            del self._storage[resume_id]
            return True
        return False


# Singleton instance
resume_model = ResumeModel()
