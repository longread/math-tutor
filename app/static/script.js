document.addEventListener('DOMContentLoaded', () => {
    const problemForm = document.getElementById('problem-form');
    const problemTextInput = document.getElementById('problem-text');
    const problemImageInput = document.getElementById('problem-image');
    const loadingDiv = document.getElementById('loading');
    const solutionContainer = document.getElementById('solution-container');
    const nextStepButton = document.getElementById('next-step-button');
    const errorMessageDiv = document.getElementById('error-message');
    const originalQuestionDiv = document.getElementById('original-question');

    let currentSteps = [];
    let currentStepIndex = 0;
    let finalAnswer = '';

    problemForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        // Clear previous results and errors
        solutionContainer.innerHTML = '';
        errorMessageDiv.style.display = 'none';
        nextStepButton.style.display = 'none';
        originalQuestionDiv.innerHTML = '';
        loadingDiv.style.display = 'block';

        const formData = new FormData();
        const problemText = problemTextInput.value;
        const problemImage = problemImageInput.files[0];

        if (problemText) {
            formData.append('problem_text', problemText);
        }
        if (problemImage) {
            formData.append('problem_image', problemImage);
        }

        if (!problemText && !problemImage) {
            errorMessageDiv.textContent = 'Please provide either text or an image for the math problem.';
            errorMessageDiv.style.display = 'block';
            loadingDiv.style.display = 'none';
            return;
        }

        try {
            const response = await fetch('/solve', {
                method: 'POST',
                body: formData,
            });

            loadingDiv.style.display = 'none';

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            currentSteps = data.steps || [];
            finalAnswer = data.final_answer || '';
            currentStepIndex = 0;

            // Display original question (if text was provided)
            if (problemText) {
                originalQuestionDiv.innerHTML = `<h3>Original Question:</h3><p>${problemText}</p>`;
            } else if (problemImage) {
                originalQuestionDiv.innerHTML = `<h3>Original Question:</h3><p><em>(Image input received)</em></p>`;
            }

            if (currentSteps.length > 0) {
                displayNextStep();
                if (currentSteps.length > 1 || (currentSteps.length === 1 && finalAnswer)) {
                    nextStepButton.style.display = 'block';
                }
            } else {
                // Handle cases where AI might politely decline or return a single statement
                solutionContainer.innerHTML = `<div class="step-card">${finalAnswer || 'No steps provided, but here is a response: ' + JSON.stringify(data)}</div>`;
            }


        } catch (error) {
            console.error('Error:', error);
            errorMessageDiv.textContent = `Error: ${error.message}`;
            errorMessageDiv.style.display = 'block';
            loadingDiv.style.display = 'none';
        }
    });

    nextStepButton.addEventListener('click', () => {
        displayNextStep();
    });

    function displayNextStep() {
        if (currentStepIndex < currentSteps.length) {
            const stepContent = currentSteps[currentStepIndex];
            const stepCard = document.createElement('div');
            stepCard.classList.add('step-card');
            stepCard.innerHTML = stepContent; // MathJax will render this later
            solutionContainer.appendChild(stepCard);
            currentStepIndex++;

            if (currentStepIndex >= currentSteps.length) {
                nextStepButton.style.display = 'none';
                if (finalAnswer) {
                    const answerCard = document.createElement('div');
                    answerCard.classList.add('final-answer-card');
                    answerCard.innerHTML = `Final Answer: ${finalAnswer}`; // MathJax will render this later
                    solutionContainer.appendChild(answerCard);
                }
            }
        }
        // Assuming MathJax will be loaded and render new content. Trigger a re-render if needed.
        if (window.MathJax) {
             MathJax.typesetPromise();
        }
    }
});