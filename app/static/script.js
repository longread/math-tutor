// Helper function to safely render MathJax
function renderMath() {
    if (window.MathJax && window.MathJax.typesetPromise) {
        MathJax.typesetPromise().catch((err) => console.log('MathJax rendering error:', err));
    } else if (window.MathJax && window.MathJax.Hub) {
        // MathJax 2.x fallback
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    }
}

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

        // Determine which button was clicked
        const submitter = event.submitter;
        const action = submitter ? submitter.value : 'solution';

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
            // Choose endpoint based on which button was clicked
            const endpoint = action === 'hint' ? '/hint' : '/solve';
            
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData,
            });

            loadingDiv.style.display = 'none';

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Display original question
            if (problemText) {
                originalQuestionDiv.innerHTML = `<h3>Original Question:</h3><p>${problemText}</p>`;
            } else if (problemImage) {
                originalQuestionDiv.innerHTML = `<h3>Original Question:</h3><p><em>(Image input received)</em></p>`;
            }

            // Handle hint response
            if (action === 'hint') {
                console.log('Hint data received:', data);
                const keyConceptsArray = data.key_concepts || [];
                const hintsArray = data.hints || [];
                console.log('Key concepts:', keyConceptsArray);
                console.log('Hints:', hintsArray);
                
                if (keyConceptsArray.length === 0 && hintsArray.length === 0) {
                    solutionContainer.innerHTML = `<div class="step-card">No hint available.</div>`;
                } else {
                    // Display key concepts
                    if (keyConceptsArray.length > 0) {
                        const conceptsHeader = document.createElement('h3');
                        conceptsHeader.textContent = '🔑 Key Concepts:';
                        conceptsHeader.style.marginTop = '0';
                        solutionContainer.appendChild(conceptsHeader);
                        
                        keyConceptsArray.forEach((concept, index) => {
                            const conceptCard = document.createElement('div');
                            conceptCard.classList.add('step-card');
                            conceptCard.innerHTML = `<strong>Concept ${index + 1}:</strong> ${concept}`;
                            solutionContainer.appendChild(conceptCard);
                        });
                    }
                    
                    // Display hints
                    if (hintsArray.length > 0) {
                        const hintsHeader = document.createElement('h3');
                        hintsHeader.textContent = '💡 Hints:';
                        solutionContainer.appendChild(hintsHeader);
                        
                        hintsArray.forEach((hint, index) => {
                            const hintCard = document.createElement('div');
                            hintCard.classList.add('step-card');
                            hintCard.innerHTML = `<strong>Hint ${index + 1}:</strong> ${hint}`;
                            solutionContainer.appendChild(hintCard);
                        });
                    }
                    
                    // Trigger MathJax rendering
                    renderMath();
                }
            } else {
                // Handle solution response
                currentSteps = data.steps || [];
                finalAnswer = data.final_answer || '';
                currentStepIndex = 0;

                if (currentSteps.length > 0) {
                    displayNextStep();
                    if (currentSteps.length > 1 || (currentSteps.length === 1 && finalAnswer)) {
                        nextStepButton.style.display = 'block';
                    }
                } else {
                    // Handle cases where AI might politely decline or return a single statement
                    solutionContainer.innerHTML = `<div class="step-card">${finalAnswer || 'No steps provided, but here is a response: ' + JSON.stringify(data)}</div>`;
                }
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
        // Trigger MathJax rendering for new content
        renderMath();
    }
});