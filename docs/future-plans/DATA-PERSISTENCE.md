# 💾 Data Persistence - Future Implementation Plan

**Status:** 📋 Planned for Future Release  
**Priority:** Medium  
**Estimated Effort:** 2-4 hours (localStorage) / 1-2 days (full database)

---

## 🎯 Goal

Enable users to accumulate survey submissions over time to unlock Advanced Analysis features (requires 10+ submissions for statistical ANOVA).

---

## 📊 Current State

### How It Works Now

- **Storage:** React `useState` (in-memory only)
- **Persistence:** ❌ None - data lost on refresh
- **Limitation:** Users must complete 10 surveys in a single session
- **Impact:** Advanced Analysis difficult to test/use

### Code Location

```typescript
// frontend/src/App.tsx
const [analysisHistory, setAnalysisHistory] = useState<AnalysisRequest[]>([]);

// Data added on submission
mutation.onSuccess((data) => {
  setResult(data);
  setAnalysisHistory(prev => [...prev, answers]);
});
```

---

## ✅ Solution Options

### Option 1: Browser localStorage (Quick Win)

**Pros:**
- ✅ Simple implementation (~2 hours)
- ✅ No backend changes required
- ✅ Works offline
- ✅ 100% private (data stays on device)
- ✅ No database setup needed

**Cons:**
- ⚠️ Per-device only (doesn't sync)
- ⚠️ Limited storage (~5-10MB)
- ⚠️ Can be cleared by user
- ⚠️ No multi-user data collection

**Best For:**
- Personal testing
- Single-user deployments
- Quick prototyping

**Implementation Estimate:** 2-3 hours

---

### Option 2: Backend Database (Full Solution)

**Pros:**
- ✅ Persistent across all devices
- ✅ Multi-user data collection
- ✅ Real research-grade analytics
- ✅ Backup and recovery
- ✅ Data export capabilities

**Cons:**
- ❌ Requires database setup (PostgreSQL/MongoDB)
- ❌ Privacy considerations (GDPR compliance)
- ❌ More complex deployment
- ❌ Requires backend API changes

**Best For:**
- Research studies
- Production deployment
- Multi-user scenarios
- Academic research

**Implementation Estimate:** 1-2 days

---

## 🚀 Recommended Implementation: Option 1 (localStorage)

### Technical Design

#### 1. Create Storage Utility

```typescript
// frontend/src/utils/storage.ts
const STORAGE_KEY = 'lgbtq_analysis_history';

export const saveAnalysisHistory = (history: AnalysisRequest[]): void => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  } catch (error) {
    console.error('Failed to save analysis history:', error);
  }
};

export const loadAnalysisHistory = (): AnalysisRequest[] => {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error('Failed to load analysis history:', error);
    return [];
  }
};

export const clearAnalysisHistory = (): void => {
  localStorage.removeItem(STORAGE_KEY);
};
```

#### 2. Update App Component

```typescript
// frontend/src/App.tsx

// Load data on mount
const [analysisHistory, setAnalysisHistory] = useState<AnalysisRequest[]>(() => {
  return loadAnalysisHistory();
});

// Save data whenever it changes
useEffect(() => {
  saveAnalysisHistory(analysisHistory);
}, [analysisHistory]);

// Add clear button in settings
const handleClearHistory = () => {
  if (confirm('Clear all saved survey data?')) {
    clearAnalysisHistory();
    setAnalysisHistory([]);
  }
};
```

#### 3. Add UI Indicators

```typescript
// Show storage status
<div className="text-xs text-gray-500">
  📊 {analysisHistory.length} survey(s) saved locally
  {analysisHistory.length > 0 && (
    <button onClick={handleClearHistory} className="ml-2 text-red-500">
      Clear Data
    </button>
  )}
</div>
```

---

## 🏗️ Option 2 Implementation (Future: Full Database)

### Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│   Browser   │────▶│   Backend   │────▶│  PostgreSQL  │
│  (React)    │     │  (FastAPI)  │     │   Database   │
└─────────────┘     └─────────────┘     └──────────────┘
```

### Database Schema

```sql
-- submissions table
CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Survey answers (JSONB for flexibility)
    answers JSONB NOT NULL,
    
    -- Calculated results
    overall_score DECIMAL(5,2),
    section_scores JSONB,
    
    -- Privacy: no personal identifiers
    ip_hash VARCHAR(64),  -- Hashed IP for rate limiting
    user_agent_hash VARCHAR(64)
);

-- Index for analytics
CREATE INDEX idx_created_at ON submissions(created_at);
CREATE INDEX idx_session_id ON submissions(session_id);
```

### Backend API Endpoints

```python
# backend/app/api/routes_submissions.py

@router.post("/submissions")
async def save_submission(
    payload: SubmissionCreate,
    db: Session = Depends(get_db)
) -> SubmissionResponse:
    """Save a survey submission anonymously."""
    submission = Submission(
        session_id=payload.session_id,
        answers=payload.answers,
        overall_score=payload.overall_score,
        section_scores=payload.section_scores
    )
    db.add(submission)
    db.commit()
    return submission

@router.get("/submissions/session/{session_id}")
async def get_session_submissions(
    session_id: str,
    db: Session = Depends(get_db)
) -> List[SubmissionResponse]:
    """Get all submissions for a session."""
    return db.query(Submission).filter(
        Submission.session_id == session_id
    ).order_by(Submission.created_at.desc()).all()
```

### Privacy Considerations

- ✅ No personal identifiers stored
- ✅ Anonymous session IDs (UUID v4)
- ✅ IP addresses hashed (one-way)
- ✅ No tracking cookies
- ✅ GDPR-compliant data deletion
- ✅ Encryption at rest (PostgreSQL)

---

## 📋 Implementation Checklist

### Phase 1: localStorage (Quick Win)

- [ ] Create `frontend/src/utils/storage.ts`
- [ ] Add load/save/clear functions
- [ ] Update `App.tsx` with localStorage hooks
- [ ] Add "Clear Data" button to UI
- [ ] Test with 10+ submissions
- [ ] Verify data persists after refresh
- [ ] Add storage size monitoring
- [ ] Update documentation

**Time Estimate:** 2-3 hours

---

### Phase 2: Backend Database (Future)

#### Backend Tasks
- [ ] Choose database (PostgreSQL recommended)
- [ ] Design database schema
- [ ] Create migration files
- [ ] Implement submission endpoints
- [ ] Add session management
- [ ] Implement rate limiting
- [ ] Add data export API
- [ ] Write unit tests

#### Frontend Tasks
- [ ] Update API client with new endpoints
- [ ] Add session ID generation
- [ ] Implement auto-save on submission
- [ ] Add sync status indicators
- [ ] Handle offline mode gracefully
- [ ] Add data export UI

#### DevOps Tasks
- [ ] Set up PostgreSQL container
- [ ] Update docker-compose.yml
- [ ] Configure environment variables
- [ ] Add database backups
- [ ] Set up monitoring

**Time Estimate:** 1-2 days

---

## 🎯 Success Metrics

### Phase 1 (localStorage)
- ✅ Data persists across browser sessions
- ✅ Users can accumulate 10+ submissions
- ✅ Advanced Analysis becomes usable
- ✅ No errors when storage is full

### Phase 2 (Database)
- ✅ 100% data persistence
- ✅ Multi-device sync working
- ✅ < 200ms API response time
- ✅ Can handle 1000+ concurrent users
- ✅ Zero data loss incidents

---

## 💡 Recommendations

### For Development/Testing
**Use localStorage** - Quick to implement, sufficient for testing

### For Production Research
**Use Database** - Required for:
- Collecting data from multiple participants
- Academic research
- Long-term studies
- Data export and analysis

### Hybrid Approach (Best of Both)
1. Start with localStorage for immediate functionality
2. Add database sync later as optional feature
3. Let users choose: "Save locally only" or "Sync to cloud"

---

## 🔗 Related Documentation

- `CHATBOT-COMPLETE.md` - Chatbot works with 1 submission (no persistence needed)
- `AI-INSIGHTS-FIX.md` - Advanced Analysis requirements
- `QUICK-START.md` - Current setup guide

---

## 📅 Timeline

| Phase | Duration | When |
|-------|----------|------|
| **localStorage** | 2-3 hours | Next sprint |
| **Database Design** | 4 hours | Month 2 |
| **Backend API** | 1 day | Month 2 |
| **Frontend Integration** | 4 hours | Month 2 |
| **Testing & QA** | 4 hours | Month 2 |

---

## ✅ Decision Deferred

**Action:** Keep localStorage implementation ready for next sprint  
**Reason:** Current focus on chatbot (works with 1 submission)  
**Next Review:** When user requests Advanced Analysis functionality

**Status:** 📋 **Documented and Ready for Implementation**
