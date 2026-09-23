const task =
    document.getElementById("task");

const inputText =
    document.getElementById("inputText");

const submitBtn =
    document.getElementById("submitBtn");

const result =
    document.getElementById("result");

const statusBox =
    document.getElementById("status");

const charCount =
    document.getElementById("charCount");

const copyBtn =
    document.getElementById("copyBtn");


// ---------------------------------------------------------
// Status
// ---------------------------------------------------------

function setStatus(
    message,
    error = false
) {

    statusBox.textContent =
        message;

    statusBox.classList.remove(
        "hidden",
        "error"
    );

    if (error) {

        statusBox.classList.add(
            "error"
        );
    }
}


function clearStatus() {

    statusBox.classList.add(
        "hidden"
    );
}


// ---------------------------------------------------------
// HTML escaping
// ---------------------------------------------------------

function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );
}


// ---------------------------------------------------------
// Render AI result
// ---------------------------------------------------------

function renderResult(data) {


    // Normal text response
    if (typeof data === "string") {

        result.classList.remove(
            "empty"
        );

        result.textContent =
            data;

        return;
    }


    // Quiz
    if (data.questions) {

        result.classList.remove(
            "empty"
        );


        result.innerHTML =
            data.questions
                .map(
                    (question, index) => `

                    <article
                        class="quiz-question"
                    >

                        <h3>
                            ${index + 1}.
                            ${escapeHtml(
                                question.question
                            )}
                        </h3>


                        ${question.options
                            .map(
                                option => `

                                <div
                                    class="option ${
                                        option ===
                                        question.correct_answer
                                            ? "correct"
                                            : ""
                                    }"
                                >
                                    ${escapeHtml(
                                        option
                                    )}
                                </div>

                            `
                            )
                            .join("")
                        }


                        <p>
                            <strong>
                                Answer:
                            </strong>

                            ${escapeHtml(
                                question.correct_answer
                            )}
                        </p>


                        <p>
                            ${escapeHtml(
                                question.explanation
                            )}
                        </p>

                    </article>

                `
                )
                .join("");

        return;
    }


    // Learning path
    if (data.steps) {

        result.classList.remove(
            "empty"
        );


        result.innerHTML = `

            <h3>
                ${escapeHtml(
                    data.topic
                )}
            </h3>


            ${data.steps
                .map(
                    (step, index) => `

                    <article
                        class="learning-step"
                    >

                        <h3>

                            ${index + 1}.

                            ${escapeHtml(
                                step.level
                            )}

                            —

                            ${escapeHtml(
                                step.topic
                            )}

                        </h3>


                        <p>

                            <strong>
                                Estimated time:
                            </strong>

                            ${escapeHtml(
                                step.estimated_time
                            )}

                        </p>


                        <p>
                            <strong>
                                Objectives
                            </strong>
                        </p>


                        <ul>

                            ${step.objectives
                                .map(
                                    item =>
                                        `<li>
                                            ${escapeHtml(item)}
                                        </li>`
                                )
                                .join("")
                            }

                        </ul>


                        <p>
                            <strong>
                                Resources
                            </strong>
                        </p>


                        <ul>

                            ${step.resources
                                .map(
                                    item =>
                                        `<li>
                                            ${escapeHtml(item)}
                                        </li>`
                                )
                                .join("")
                            }

                        </ul>

                    </article>

                `
                )
                .join("")
            }


            <h3>
                Study Tips
            </h3>


            <ul>

                ${data.study_tips
                    .map(
                        tip =>
                            `<li>
                                ${escapeHtml(tip)}
                            </li>`
                    )
                    .join("")
                }

            </ul>
        `;

        return;
    }


    // Fallback JSON
    result.classList.remove(
        "empty"
    );

    result.textContent =
        JSON.stringify(
            data,
            null,
            2
        );
}


// ---------------------------------------------------------
// Character counter
// ---------------------------------------------------------

inputText.addEventListener(
    "input",
    () => {

        charCount.textContent =
            `${inputText.value.length} / 20000`;

    }
);


// ---------------------------------------------------------
// Copy result
// ---------------------------------------------------------

copyBtn.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                result.innerText
            );

            setStatus(
                "Result copied to clipboard."
            );

            setTimeout(
                clearStatus,
                1500
            );

        } catch {

            setStatus(
                "Could not copy the result.",
                true
            );
        }
    }
);


// ---------------------------------------------------------
// Main submit
// ---------------------------------------------------------

submitBtn.addEventListener(
    "click",
    async () => {

        const text =
            inputText.value.trim();


        if (!text) {

            setStatus(
                "Please enter a question, topic, or passage.",
                true
            );

            return;
        }


        submitBtn.disabled =
            true;

        copyBtn.disabled =
            true;


        result.classList.add(
            "empty"
        );


        result.textContent =
            "EduGenie is thinking...";


        setStatus(
            "Generating your learning result..."
        );


        try {

            const response =
                await fetch(
                    "/api/task",
                    {

                        method:
                            "POST",

                        headers: {

                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                task:
                                    task.value,

                                text:
                                    text

                            })

                    }
                );


            const contentType =
                response.headers.get("content-type") || "";

            const body =
                contentType.includes("application/json")
                    ? await response.json()
                    : await response.text();


            if (!response.ok) {

                const errorMessage =
                    typeof body === "string"
                        ? body
                        : body.detail;

                throw new Error(
                    errorMessage ||
                    "The server returned an error."
                );
            }


            renderResult(
                body.result
            );


            copyBtn.disabled =
                false;


            setStatus(
                "Done."
            );


            setTimeout(
                clearStatus,
                1500
            );


        } catch (error) {

            result.classList.add(
                "empty"
            );


            result.textContent =
                "Unable to generate a result.";


            setStatus(
                error.message,
                true
            );


        } finally {

            submitBtn.disabled =
                false;
        }
    }
);