# Technical Interview Questions: Self-Healing Automation Framework

This document contains a set of technical interview questions designed to assess a candidate's understanding of the Self-Healing Automation Framework. The questions cover architecture, design patterns, implementation details, and potential improvements.

---

### Q1: High-Level Architecture

**Question:** Can you describe the high-level architecture of this framework? What are the main components and how do they interact?

**Answer:**
The framework is composed of two primary components:

1.  **`SafePage`**: This is a wrapper class around Playwright's standard `Page` object. Its role is to intercept common actions like `click()` and `fill()`. When one of these actions fails due to a `TimeoutError` (meaning the selector didn't find an element), it triggers the self-healing process instead of immediately failing the test.

2.  **`OpenAIHealer`**: This class is responsible for the "healing" logic. It communicates with the Azure OpenAI service. When `SafePage` triggers the healing process, it passes the failed selector, the current DOM of the page, and the error message to the `OpenAIHealer`. The healer then constructs a detailed prompt asking the LLM to analyze the information and suggest a corrected, more robust selector.

The interaction is as follows:
- An action is called on a `SafePage` instance (e.g., `safe_page.click("#my-button")`).
- `SafePage` attempts the action using the underlying Playwright `page` object.
- If it fails with a `TimeoutError`, `SafePage` catches the exception.
- It captures a snapshot of the page's DOM and calls `OpenAIHealer.get_new_selector()`.
- The `OpenAIHealer` sends a request to the Azure OpenAI API and gets back a suggested new selector.
- `SafePage` retries the original action with the new selector.
- If the retry is successful, the process is complete. If it fails again, a final exception is raised.

---

### Q2: `OpenAIHealer` Deep Dive

**Question:** Looking at `openai_healer.py`, what is the purpose of the "system prompt"? Why is it important for the reliability of the healing process?

**Answer:**
The system prompt (`system_prompt`) serves to set the context and define the persona for the AI model. In this case, it instructs the LLM to act as a "Senior QA Engineer and Playwright expert."

This is crucial for several reasons:
1.  **Role-Specific Expertise:** It primes the model to think in the context of test automation, selectors, and front-end structure, leading to more accurate and relevant suggestions. It knows to prefer CSS or text-based selectors because the prompt tells it to.
2.  **Output Formatting:** The prompt explicitly states the rules for the output: "Return ONLY the corrected selector string, nothing else." This is critical for programmatic use, as it prevents the LLM from returning conversational text, explanations, or code blocks that would need to be parsed and cleaned.
3.  **Behavioral Guardrails:** It provides guidelines on what makes a good selector (e.g., "specific and unlikely to match multiple elements") and what common issues to look for (dynamic IDs, changed class names). This steers the model away from naive suggestions and towards more robust solutions.

Without a well-defined system prompt, the LLM's response would be far less predictable and reliable, making it difficult to integrate into an automated workflow.

---

### Q3: `SafePage` Implementation

**Question:** In `safe_page.py`, why are methods like `goto()` and `screenshot()` implemented as simple pass-throughs, while `click()` and `fill()` have detailed healing logic?

**Answer:**
The distinction is based on the type of error each method is likely to encounter.

-   `click()` and `fill()` are action-based methods that operate on selectors. The most common reason for their failure in a changing UI is a broken or outdated selector, which is exactly what the self-healing mechanism is designed to fix. Therefore, they contain the `try...except PlaywrightTimeoutError` block to handle this specific failure scenario.

-   `goto()`, `screenshot()`, `wait_for_selector()`, and `close()` are different.
    -   `goto(url)` fails if a URL is unreachable, not because of a bad selector.
    -   `screenshot()` might fail due to file system issues, not a selector.
    -   `close()` is a cleanup action.
    -   `wait_for_selector()` could be enhanced with healing, but its primary purpose is waiting, not interacting.

By implementing healing logic only for action-based methods that depend on selectors, the framework remains focused and efficient. The pass-through methods ensure that `SafePage` still behaves like a regular `Page` object for all other operations, making it a non-intrusive wrapper.

---

### Q4: Error Handling and Reliability

**Question:** What happens if the AI's suggested selector also fails? How does the framework prevent infinite loops or silent failures?

**Answer:**
This is a critical aspect of the framework's design. The healing process is not a guaranteed fix, and the implementation accounts for this:

1.  **Single Retry:** The healing logic attempts a fix only **once**. As seen in `SafePage.click()`, if the original selector fails, it gets one new selector and retries. If that retry also fails, an exception is immediately raised. There is no loop.

2.  **Explicit Failure:** When the healed selector also fails, the exception raised is very descriptive. It includes the original selector, the AI-suggested selector, and the error from the healing attempt. This provides a clear audit trail for a developer to debug the problem, showing both what was tried and why it failed.

3.  **Healing API Failure:** The framework also wraps the call to the healer (`self.healer.get_new_selector(...)`) in its own `try...except` block. If the Azure OpenAI API call fails for any reason (e.g., network issue, invalid API key), it raises an exception immediately, preventing the test from hanging.

This approach ensures that the self-healing feature is an enhancement, not a source of instability. It gets one chance to fix the problem, and if it can't, it fails fast with a clear error.

---

### Q5: Extensibility and Future Improvements

**Question:** The `README.md` mentions that a potential improvement would be to "implement selector caching." How would you design and implement such a feature? What would be the benefits?

**Answer:**
Implementing selector caching would be a significant improvement to optimize both performance and cost.

**Design:**

1.  **Cache Storage:** I would implement a simple in-memory dictionary or a more persistent key-value store (like a file-based cache using `shelve` or `pickle`) to store the mappings of broken selectors to healed selectors. The key would be the `old_selector`, and the value would be the `new_selector`.

2.  **Cache Location:** This cache could be managed within the `OpenAIHealer` or as a separate `HealingCache` class that the `SafePage` can access. Managing it in the healer is likely cleaner.

3.  **Workflow Modification:** The `SafePage`'s healing logic would be updated:
    -   When a selector fails, it first checks the cache: `cached_selector = cache.get(old_selector)`.
    -   If a `cached_selector` is found, it uses it directly for the retry. This avoids the API call entirely.
    -   If the selector is not in the cache, it proceeds to call the `OpenAIHealer`.
    -   If the `OpenAIHealer` successfully finds a new selector and the subsequent action succeeds, the mapping is stored in the cache: `cache.set(old_selector, new_selector)`.

**Implementation in `SafePage.py` (pseudo-code):**

```python
# In the `except PlaywrightTimeoutError` block of click()

# 1. Check cache first
healed_selector = self.cache.get(selector)
if healed_selector:
    print(f"[HEALING] Found healed selector in cache: {healed_selector}")
    try:
        self.page.click(healed_selector, ...)
        print("HEALED (from cache): ...")
        return # Success
    except PlaywrightTimeoutError:
        print("[HEALING] Cached selector failed. Re-healing...")
        # Proceed to AI healing, and overwrite cache on success
        
# 2. If not in cache, call AI
new_selector = self.healer.get_new_selector(...)

# 3. On success, update cache
self.page.click(new_selector, ...)
self.cache.set(selector, new_selector) # Store the successful mapping
```

**Benefits:**

-   **Cost Reduction:** This would dramatically reduce costs by minimizing the number of calls to the Azure OpenAI API. A selector that breaks once would be fixed for the entire duration of the test suite run.
-   **Performance Improvement:** An API call to an LLM can take several seconds. A local cache lookup is nearly instantaneous, making the healing process much faster for known broken selectors.
-   **Increased Determinism:** Relying on a cached, previously successful selector is more deterministic than asking the LLM for a new suggestion every time.
