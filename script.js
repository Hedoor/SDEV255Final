const courses = [
    {
        code: "1",
        name: "temp",
        description: "temp",
        subject: "temp",
        credits: 3
    },
    {
        code: "2",
        name: "temp",
        description: "temp",
        subject: "temp",
        credits: 3
    },
    {
        code: "3",
        name: "temp",
        description: "temp",
        subject: "temp",
        credits: 3
    },
];

// selected courses
let selectedCourses = [];

const courseTableBody = document.getElementById('course-table-body');
const selectedCoursesList = document.getElementById('selected-courses-list');
const totalCreditsElement = document.getElementById('total-credits');

function init() {
    renderCourseTable();
    renderSelectedCourses();
}

// render course table
function renderCourseTable() {
    courseTableBody.innerHTML = '';
    
    courses.forEach(course => {
        const isSelected = selectedCourses.some(selected => selected.code === course.code);
        
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${course.code}</td>
            <td>${course.name}</td>
            <td>${course.description}</td>
            <td>${course.subject}</td>
            <td>${course.credits}</td>
            <td>
                <button class="${isSelected ? 'remove' : ''}" 
                        data-code="${course.code}">
                    ${isSelected ? 'Drop' : 'Add'}
                </button>
            </td>
        `;
        
        courseTableBody.appendChild(row);
    });
    
    // button listeners
    document.querySelectorAll('#course-table-body button').forEach(button => {
        button.addEventListener('click', handleCourseAction);
    });
}

// render selected courses
function renderSelectedCourses() {
    selectedCoursesList.innerHTML = '';
    
    if (selectedCourses.length === 0) {
        selectedCoursesList.innerHTML = '<p>No courses selected yet.</p>';
        totalCreditsElement.textContent = 'Total Credits: 0';
        return;
    }
    
    let totalCredits = 0;
    
    selectedCourses.forEach(course => {
        totalCredits += course.credits;
        
        const courseItem = document.createElement('div');
        courseItem.className = 'selected-course-item';
        courseItem.innerHTML = `
            <div>
                <strong>${course.code}</strong>: ${course.name} (${course.credits} credits)
            </div>
            <button class="remove" data-code="${course.code}">Remove</button>
        `;
        
        selectedCoursesList.appendChild(courseItem);
    });
    
    totalCreditsElement.textContent = `Total Credits: ${totalCredits}`;
    
    // listeners for remove button
    document.querySelectorAll('.selected-course-item button').forEach(button => {
        button.addEventListener('click', handleCourseAction);
    });
}

// add/drop
function handleCourseAction(event) {
    const courseCode = event.target.getAttribute('data-code');
    const course = courses.find(c => c.code === courseCode);
    
    if (event.target.classList.contains('remove')) {
        // remove
        selectedCourses = selectedCourses.filter(c => c.code !== courseCode);
    } else {
        // add
        if (!selectedCourses.some(c => c.code === courseCode)) {
            selectedCourses.push(course);
        }
    }
    
    // view updater
    renderCourseTable();
    renderSelectedCourses();
    
    // button listeners
    document.querySelectorAll('#course-table-body button').forEach(button => {
        button.addEventListener('click', handleCourseAction);
    });
}

// navbar stuff
document.getElementById('edit-btn').addEventListener('click', editCourse);
document.getElementById('delete-btn').addEventListener('click', deleteCourse);
document.getElementById('logout-btn').addEventListener('click', logOut);

// edit
function editCourse() {
    window.location.href = "edit.html";
}

// delete
function deleteCourse() {
    window.location.href = "delete.html";
}

// logout
function logOut() {
    window.location.href = "logout.html";
}

document.addEventListener('DOMContentLoaded', init);