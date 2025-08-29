from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from ..models import JobApplication, JobApplicationCreate, JobApplicationUpdate, JobApplicationRead, ApplicationStatus, User
from ..database import get_session
from ..auth import get_current_user

router = APIRouter(prefix="/applications", tags=["job-applications"])


@router.post("/", response_model=JobApplicationRead)
def create_job_application(
    application: JobApplicationCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Add new job application"""
    db_application = JobApplication(
        **application.dict(),
        user_id=current_user.id
    )
    session.add(db_application)
    session.commit()
    session.refresh(db_application)
    return db_application


@router.get("/", response_model=List[JobApplicationRead])
def get_job_applications(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all job applications for the current user"""
    applications = session.exec(
        select(JobApplication)
        .where(JobApplication.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    ).all()
    return applications


@router.get("/search", response_model=List[JobApplicationRead])
def search_job_applications(
    status: Optional[ApplicationStatus] = Query(None, description="Filter by application status"),
    company: Optional[str] = Query(None, description="Filter by company name"),
    position: Optional[str] = Query(None, description="Filter by position"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Search job applications with filters"""
    try:
        query = select(JobApplication).where(JobApplication.user_id == current_user.id)

        if status:
            query = query.where(JobApplication.status == status)

        if company:
            query = query.where(JobApplication.company.contains(company))

        if position:
            query = query.where(JobApplication.position.contains(position))

        applications = session.exec(query).all()
        return applications

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid query parameters: {str(e)}"
        )


@router.get("/{application_id}", response_model=JobApplicationRead)
def get_job_application(
    application_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific job application"""
    application = session.exec(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id
        )
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Job application not found")

    return application


@router.put("/{application_id}", response_model=JobApplicationRead)
def update_job_application(
    application_id: int,
    application_update: JobApplicationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a job application"""
    application = session.exec(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id
        )
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Job application not found")

    application_data = application_update.dict(exclude_unset=True)
    for field, value in application_data.items():
        setattr(application, field, value)

    session.add(application)
    session.commit()
    session.refresh(application)
    return application


@router.delete("/{application_id}")
def delete_job_application(
    application_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a job application"""
    application = session.exec(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id
        )
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Job application not found")

    session.delete(application)
    session.commit()
    return {"message": "Job application deleted successfully"}
