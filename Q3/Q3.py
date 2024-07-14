import time
import copy

class Repository:
    def __init__(self, name):
        self.name = name
        self.branches = {'main': []}
        self.current_branch = 'main'
        self.commit_history = {'main': []}
        self.file_tree = {'main': {}}

def create_repository(name):
    return Repository(name)


def commit(repository, message, changes):
    timestamp = time.time()
    new_tree = copy.deepcopy(repository.file_tree[repository.current_branch])
    new_tree.update(changes)
    repository.file_tree[repository.current_branch] = new_tree
    commit_data = {
        'message': message,
        'timestamp': timestamp,
        'tree': new_tree
    }
    repository.commit_history[repository.current_branch].append(commit_data)

# Example usage
repo = create_repository("MyRepo")
commit(repo, "Initial commit", {"dir/file1.txt": "Hello, World!"})


def create_branch(repository, branch_name):
    repository.branches[branch_name] = repository.branches[repository.current_branch]
    repository.commit_history[branch_name] = repository.commit_history[repository.current_branch]
    repository.file_tree[branch_name] = copy.deepcopy(repository.file_tree[repository.current_branch])

def switch_branch(repository, branch_name):
    if branch_name in repository.branches:
        repository.current_branch = branch_name
    else:
        raise ValueError("Branch does not exist")

# Example usage
create_branch(repo, "feature-branch")
switch_branch(repo, "feature-branch")
commit(repo, "Added new feature", {"dir/file2.txt": "New feature content"})


def merge_branch(repository, source_branch, target_branch):
    source_tree = repository.file_tree[source_branch]
    target_tree = repository.file_tree[target_branch]
    conflicts = []
    for path, content in source_tree.items():
        if path in target_tree and target_tree[path] != content:
            conflicts.append((path, content, target_tree[path]))
        else:
            target_tree[path] = content

    if conflicts:
        return conflicts  # Return conflicts to be resolved

    repository.file_tree[target_branch] = target_tree
    repository.commit_history[target_branch].append({
        'message': f'Merged {source_branch} into {target_branch}',
        'timestamp': time.time(),
        'tree': target_tree
    })

def resolve_conflict(repository, conflict_id, resolution):
    path, source_content, target_content = conflict_id
    repository.file_tree[repository.current_branch][path] = resolution
    repository.commit_history[repository.current_branch].append({
        'message': f'Resolved conflict on {path}',
        'timestamp': time.time(),
        'tree': repository.file_tree[repository.current_branch]
    })

# Example usage
conflicts = merge_branch(repo, "main", "feature-branch")
if conflicts:
    resolve_conflict(repo, conflicts[0], "Resolved content")


def view_commit_history(repository, branch_name):
    for commit in repository.commit_history[branch_name]:
        print(f"Message: {commit['message']}")
        print(f"Timestamp: {time.ctime(commit['timestamp'])}")
        print(f"Tree: {commit['tree']}")
        print("-----")

def view_file_history(repository, file_path):
    for branch, history in repository.commit_history.items():
        for commit in history:
            if file_path in commit['tree']:
                print(f"Branch: {branch}")
                print(f"Message: {commit['message']}")
                print(f"Timestamp: {time.ctime(commit['timestamp'])}")
                print(f"Content: {commit['tree'][file_path]}")
                print("-----")

# Example usage
view_commit_history(repo, "main")
view_file_history(repo, "dir/file1.txt")


# Initialize repository
repo = create_repository("MyRepo")

# Commit changes to various files and directories
commit(repo, "Initial commit", {"dir/file1.txt": "Hello, World!"})
commit(repo, "Second commit", {"dir/file2.txt": "Second file content"})

# Create a new branch and make additional changes
create_branch(repo, "feature-branch")
switch_branch(repo, "feature-branch")
commit(repo, "Feature commit", {"dir/file3.txt": "Feature branch content"})

# Switch between branches
switch_branch(repo, "main")
commit(repo, "Main branch commit", {"dir/file1.txt": "Updated content in main branch"})

# Merge branches and resolve conflicts
conflicts = merge_branch(repo, "feature-branch", "main")
if conflicts:
    resolve_conflict(repo, conflicts[0], "Resolved content for conflict")

# View commit history and file history
view_commit_history(repo, "main")
view_file_history(repo, "dir/file1.txt")


