# GitHub Project Management and Collaboration Workflow
## CO7095 – Software Measurement and Quality Assurance (2026–2027)
### News Monitoring and Analytics Application

---

## 1. Repository Setup and Administration

### 1.1 Repository Information
- **Repository Name**: `NewsMonitoringAnalytics-CO7095`
- **Visibility**: Private (during active coursework development) or as mandated by module convenors.
- **Default Branch**: `main`
- **Integration Branch**: `develop`

### 1.2 Team Access & Collaborator Permissions
To establish the collaborative development environment:
1. Navigate to **GitHub Repository** -> **Settings** -> **Collaborators and teams**.
2. Click **Add people** and invite all four group members:
   - Nikitha Sarpur (`ns713`)
   - Sashi Dommaraju (`Sd683`)
   - Jyothi Bandalapati (`Jb1080`)
   - Jalakam Prashanth (`Pj161`)
3. Assign **Write** or **Admin** permissions to group members to permit branch pushes and review assignments.
4. Invite Course Instructors, Professors, and Graduate Teaching Assistants (TAs) using their official University of Leicester GitHub usernames as requested in the module handbook (assigning **Read** or **Triage** permissions). *Note: Instructors and TAs must be added using their specific university accounts as notified via Blackboard.*

---

## 2. GitHub Projects Board & Issue Tracking

The team tracks sprint progress using **GitHub Projects (Boards)**:
1. **Columns**:
   - `Backlog`: Stories pending future sprints.
   - `Sprint Backlog`: Stories committed for the current sprint.
   - `In Progress`: Stories actively being coded on dedicated feature branches.
   - `In Review / QA`: Pull Request submitted, automated tests running, peer review underway.
   - `Done`: Acceptance criteria satisfied, 100% test pass rate, merged into `develop` or `main`.

### 2.1 Issue Creation & Milestone Mapping
Every User Story maps directly to a discrete GitHub Issue.
- **Issue Title Format**: `[USxx] <Story Title>` (e.g., `[US01] Implement standardized NewsArticle domain model`)
- **Labels**: `sprint-1`, `sprint-2`, `sprint-3`, `enhancement`, `testing`, `documentation`, `member:ns713`, `member:sd683`, `member:jb1080`, `member:pj161`.
- **Milestones**:
  - `Sprint 1 - Application Backbone` (Due: End of Week 2)
  - `Sprint 2 - Monitoring & Analytics` (Due: End of Week 4)
  - `Sprint 3 - Integration, Reporting, & Quality` (Due: End of Week 6)

---

## 3. Branching Strategy and Naming Conventions

The project adheres to a simplified **GitFlow** branching strategy:

```
[main] -----------------------------------------------* (v1.0 Release)
          \                                         /
[develop]  *-------*-------*-------*-------*-------* (Sprint Integration)
            \     / \     /         \     /
[feature]    *---*   *---*           *---*
            (US01)  (US04)          (US16)
```

- **`main`**: Production-ready, stable codebase. Tagged with releases (`v1.0.0`).
- **`develop`**: Primary integration branch where sprint feature branches merge after passing reviews and tests.
- **Feature Branches**: Branch from `develop` and follow the pattern:
  `feature/US<StoryID>-<short-description>`

### Representative Feature Branch Mappings:
- `feature/US01-news-article-model` (Assigned: ns713)
- `feature/US04-news-search` (Assigned: Sd683)
- `feature/US10-keyword-monitoring-rules` (Assigned: Pj161)
- `feature/US13-rss-feed-collection` (Assigned: ns713)
- `feature/US16-sentiment-analysis` (Assigned: Sd683)
- `feature/US19-trending-topics` (Assigned: Jb1080)
- `feature/US20-duplicate-similarity-report` (Assigned: Jb1080)
- `feature/US22-keyword-alerts` (Assigned: Pj161)
- `feature/US27-offline-demo-dataset` (Assigned: ns713)
- `feature/US31-time-based-analytics` (Assigned: Jb1080)
- `feature/US36-final-cli-integration` (Assigned: Pj161)

*Note: In accordance with academic audit guidelines, keep merged branches unless the assignment explicitly permits branch deletion.*

---

## 4. Git Commands Quick Reference

### 4.1 Cloning the Repository
```bash
# Clone the repository onto your lab computer
git clone https://github.com/YourTeamOrg/NewsMonitoringAnalytics-CO7095.git
cd NewsMonitoringAnalytics-CO7095
```

### 4.2 Creating and Switching to a Feature Branch
```bash
# Ensure you are on latest develop branch
git checkout develop
git pull origin develop

# Create and checkout a new feature branch for your assigned story
git checkout -b feature/US01-news-article-model
```

### 4.3 Staging, Committing, and Pushing Changes
```bash
# Check status of modified files
git status

# Stage specific files (avoid git add . to prevent committing cache files)
git add models/article.py ns713/test/blackbox/test_article_blackbox.py

# Commit with a meaningful message referencing the story issue ID
git commit -m "[US01] Implement NewsArticle model and input validation tests"

# Push branch to remote repository
git push -u origin feature/US01-news-article-model
```

### 4.4 Creating Pull Requests and Conducting Reviews
1. Go to repository on GitHub and click **Compare & pull request**.
2. Set base branch to `develop` and compare branch to your feature branch.
3. Reference the issue in PR description: `Closes #1`.
4. Assign at least one peer team member as **Reviewer**.
5. Ensure all unit tests run cleanly on local workstation before requesting review:
   ```bash
   python run_tests.py
   ```
6. The peer reviewer inspects code diffs, verifies acceptance criteria, approves the PR, and performs a squash or standard merge into `develop`.

### 4.5 Updating Local Branch and Merging
```bash
# Switch to develop and pull merged changes
git checkout develop
git pull origin develop
```

### 4.6 Merge Conflict Resolution Procedure
If two members touch overlapping lines:
```bash
# On your feature branch, merge the latest develop
git checkout feature/USxx-your-feature
git merge develop

# Git will flag conflicts (e.g., CONFLICT in services/news_service.py)
# Open the conflicting file in PyCharm, resolve conflict markers (<<<<<<<, =======, >>>>>>>)
# Verify application runs and tests pass
python run_tests.py

# Stage resolved file and commit
git add services/news_service.py
git commit -m "Resolve merge conflict with develop branch"
git push origin feature/USxx-your-feature
```
