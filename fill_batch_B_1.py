import os

def write_and_commit(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch B)"')

files = {}

files["02-deep-learning/tensors.md"] = """# Tensors

## 1. Definition
A tensor is a multi-dimensional mathematical array used as the fundamental data structure in deep learning frameworks to encode scalars, vectors, matrices, and higher-dimensional data.

## 2. Intuition
Think of a scalar as a point, a vector as a line, a matrix as a flat spreadsheet, and a tensor as a multi-level filing cabinet. A 3D tensor is like a book of spreadsheets; a 4D tensor is a bookshelf of books.

## 3. Why it exists
Neural networks require massive, parallelized matrix multiplications. Tensors exist as the standardized abstraction that allows hardware (GPUs/TPUs) to seamlessly process these operations across any number of dimensions in contiguous memory.

## 4. Mechanics
Tensors are defined by their `rank` (number of dimensions), `shape` (size of each dimension), and `dtype` (data type). E.g., an RGB image is a 3D tensor `[Height, Width, Channels]`. A batch of images is a 4D tensor `[Batch, Height, Width, Channels]`. 

## 5. Complexity (Time & Space)
- **Time Complexity:** Element-wise ops: $O(N)$ where $N$ is total elements. Matrix mult (2D): $O(N^3)$ naive, heavily optimized on GPU.
- **Space Complexity:** $O(N) \\times$ size of dtype (e.g., float32 = 4 bytes per element).

## 6. Tiny worked example
Scalar (Rank 0): `5`
Vector (Rank 1): `[1, 2]` (Shape `[2]`)
Matrix (Rank 2): `[[1, 2], [3, 4]]` (Shape `[2, 2]`)
3D Tensor: `[[[1, 2]], [[3, 4]]]` (Shape `[2, 1, 2]`)

## 7. Code (Python, with type hints)
```python
import torch

# Create a 2D tensor (Matrix)
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32)
# Matrix multiplication
y = x @ x
```

## 8. Common mistakes
- Confusing Rank (number of axes) with Shape (size along axes).
- Forgetting that tensor operations on GPUs require contiguous memory layouts for peak speed.

## 9. 30-second interview answer
"Tensors are N-dimensional arrays used in deep learning. They generalize scalars (0D), vectors (1D), and matrices (2D) into higher dimensions. They are essential because they allow batched operations to be heavily parallelized on hardware accelerators like GPUs."

## 10. 2-minute interview answer
"Tensors are the foundational data structure of modern AI. Mathematically, they represent multilinear maps, but in computer science, they are just contiguous multi-dimensional arrays characterized by rank, shape, and data type. By organizing data into tensors—like representing a batch of text as `[Batch, Sequence_Length, Embedding_Dim]`—we avoid python `for` loops and instead dispatch single, massive BLAS (Basic Linear Algebra Subprograms) instructions to the GPU. This hardware parallelization is what makes training large neural networks computationally feasible."

## 11. Follow-ups
- "What is Broadcasting?" (Automatically expanding smaller tensors to match the shape of larger ones during arithmetic).

## 12. Deeper questions
- "How does memory stride relate to tensor contiguity?" (Strides define how many bytes to skip in memory to reach the next element in a dimension. A tensor is contiguous if its strides match the physical memory layout).

## 13. Related concepts
- **Vectors/Matrices**: Subsets of Tensors.
- **Embeddings**: Usually represented as 2D or 3D Tensors.

## 14. When it breaks / Edge cases
- Out of Memory (OOM) errors occur if tensor dimensions (like Batch Size) exceed GPU VRAM.

## 15. Comparison with alternative approaches
- **vs Python Lists:** Lists are pointers to scattered objects. Tensors are strict, contiguous blocks of numbers, enabling SIMD operations.

---
*Where this shows up in ML:* 
Every layer in PyTorch or TensorFlow takes a tensor as input and outputs a tensor.
"""

files["00-foundations/vectors-matrices.md"] = """# Vectors and Matrices

## 1. Definition
A vector is a 1D array representing magnitude and direction. A matrix is a 2D array of numbers representing a linear transformation or a dataset.

## 2. Intuition
A vector is an arrow in space; it tells you where to go. A matrix is a machine that takes an arrow and stretches, rotates, or squishes it into a new arrow.

## 3. Why it exists
They form the mathematical foundation of Linear Algebra, allowing us to concisely represent and solve systems of linear equations and transform geometric spaces, which is exactly what a neural network layer does.

## 4. Mechanics
- **Dot Product (Vectors):** Sum of element-wise products. Measures alignment (similarity).
- **Matrix Multiplication:** Applies the transformation of a matrix to a vector (or another matrix). To multiply $A (m \\times n)$ and $B (n \\times p)$, the inner dimensions ($n$) must match, yielding $(m \\times p)$.

## 5. Complexity (Time & Space)
- **Time Complexity:** Dot product of length $N$: $O(N)$. Matrix mult of two $N \\times N$ matrices: $O(N^3)$ (Strassen's is slightly better).
- **Space Complexity:** $O(N)$ for vectors, $O(N \\times M)$ for matrices.

## 6. Tiny worked example
Vector $v = [1, 2]$
Matrix $M = [[2, 0], [0, 2]]$ (A scaling matrix).
$M \\times v = [(2\\times 1 + 0\\times 2), (0\\times 1 + 2\\times 2)] = [2, 4]$. The vector was scaled by 2.

## 7. Code (Python, with type hints)
```python
import numpy as np

v1 = np.array([1, 2])
v2 = np.array([3, 4])
dot_product = np.dot(v1, v2)  # 1*3 + 2*4 = 11

M = np.array([[1, 2], [3, 4]])
transformed = M @ v1          # Matrix multiplication
```

## 8. Common mistakes
- Misaligning dimensions during matrix multiplication (the inner dimensions must match).
- Confusing element-wise multiplication (Hadamard product) with true matrix multiplication.

## 9. 30-second interview answer
"Vectors are 1D arrays representing points or directions, and matrices are 2D arrays representing linear transformations. In ML, datasets are matrices where rows are samples and columns are features, and layers apply matrix multiplications to transform these features."

## 10. 2-minute interview answer
"In ML, we use vectors to represent individual data points (like word embeddings) and matrices to represent entire datasets or the trainable weights of a neural network layer. When data passes through a Linear layer, we are simply performing matrix multiplication: transforming the input vector space into a new, learned vector space. The dot product between vectors is especially crucial, as it mathematically encodes the cosine similarity—or how 'aligned' two vectors are—which is the core mechanism behind Attention mechanisms in Transformers and similarity search in Vector Databases."

## 11. Follow-ups
- "What is an identity matrix?" (A square matrix with 1s on the diagonal, which leaves vectors unchanged when multiplied).

## 12. Deeper questions
- "What are Eigenvectors?" (Vectors that do not change direction when a specific linear transformation (matrix) is applied to them, only their magnitude scales by the eigenvalue).

## 13. Related concepts
- **Tensors**: Generalization of vectors and matrices.
- **Cosine Similarity**: Derived directly from the dot product.

## 14. When it breaks / Edge cases
- Singular (non-invertible) matrices break algorithms that require matrix inversion (like exact OLS regression).

## 15. Comparison with alternative approaches
- N/A - they are foundational mathematics.

---
*Where this shows up in ML:* 
Weight matrices $W$ in every `nn.Linear(in, out)` layer.
"""

files["02-deep-learning/forward-propagation.md"] = """# Forward Propagation

## 1. Definition
Forward propagation is the process of passing input data through a neural network's layers to generate an output prediction.

## 2. Intuition
It's an assembly line. Raw materials (data) enter the factory. The first station processes it and passes it to the next. This continues until the finished product (prediction) comes out the other end. No one looks backward during this phase.

## 3. Why it exists
Neural networks are composite functions $f(g(h(x)))$. Forward propagation exists to explicitly compute the final value of this nested function from the inside out (from input $x$ to output).

## 4. Mechanics
1. Data $X$ is multiplied by layer weights $W_1$ and bias $b_1$ is added: $Z_1 = X W_1 + b_1$.
2. An activation function $\\sigma$ is applied: $A_1 = \\sigma(Z_1)$.
3. $A_1$ becomes the input for the next layer.
4. This repeats until the final layer outputs the prediction $\\hat{Y}$.
5. Intermediate activations ($Z$ and $A$) are saved in memory for use later in Backpropagation.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(W)$ where $W$ is the total number of parameters (weights) in the network.
- **Space Complexity:** $O(A)$ where $A$ is the memory required to store all intermediate activations (crucial for training, omitted for inference).

## 6. Tiny worked example
Input $x = 2$, Weight $w = 3$, Bias $b = -1$.
Linear step: $z = 2 \\times 3 - 1 = 5$.
ReLU Activation: $\\max(0, 5) = 5$.
Prediction = 5.

## 7. Code (Python, with type hints)
```python
import numpy as np

def forward_pass(x: np.ndarray, w: np.ndarray, b: np.ndarray) -> np.ndarray:
    z = np.dot(x, w) + b
    # ReLU activation
    a = np.maximum(0, z)
    return a
```

## 8. Common mistakes
- Forgetting that intermediate activations must be stored during training, which is why training takes much more VRAM than inference.
- Dimension mismatches between $X$ and $W$.

## 9. 30-second interview answer
"Forward propagation is the inference step of a neural network. It calculates the output by sequentially applying linear transformations and non-linear activation functions to the input data, caching intermediate values if training."

## 10. 2-minute interview answer
"Forward propagation is the computational realization of the neural network's hypothesis function. Given input data, we compute the dot product with the weight matrices, add biases, and pass the result through non-linear activations layer by layer. If we are in inference mode, we discard intermediate activations to save memory. However, during training, we must cache these activations in a computational graph, because the Chain Rule during Backpropagation requires the forward values to compute local gradients. Thus, forward propagation isn't just about getting a prediction; it's about setting up the necessary state for the backward pass."

## 11. Follow-ups
- "Why do we need non-linear activations?" (Without them, the entire network collapses into a single linear transformation, regardless of depth).

## 12. Deeper questions
- "How does `torch.no_grad()` save memory?" (It prevents the framework from saving the intermediate activations and building the computational graph during the forward pass).

## 13. Related concepts
- **Backpropagation**: The reverse process that updates weights.
- **Loss Functions**: Evaluates the output of the forward pass.

## 14. When it breaks / Edge cases
- If weights are too large, forward propagation can result in `NaN`s or `Inf`s due to numerical overflow (exploding activations).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The `.forward()` method in every PyTorch `nn.Module`.
"""

files["02-deep-learning/loss-functions.md"] = """# Loss Functions

## 1. Definition
A loss function (or cost function) quantifies the difference between a model's predicted output and the actual ground-truth label.

## 2. Intuition
It's a grading rubric. If a student guesses an answer, the teacher uses the rubric to assign a penalty score based on how wrong the guess was. The goal of the student (model) is to get a score of zero.

## 3. Why it exists
Optimization algorithms (like Gradient Descent) need a singular, differentiable mathematical objective to minimize. You can't just tell a model to "do better"; you must provide a mathematical landscape where "down" means "better".

## 4. Mechanics
- **Regression (MSE):** Mean Squared Error. Calculates the average squared difference between predictions and targets. Heavily penalizes large outliers.
- **Classification (Cross-Entropy):** Calculates the divergence between the predicted probability distribution and the true one-hot distribution. Uses logarithms to heavily penalize confident wrong answers.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ where $N$ is the batch size (calculated element-wise).
- **Space Complexity:** $O(N)$ to store the gradient of the loss.

## 6. Tiny worked example
MSE: Target = 10, Prediction = 8.
Loss = $(10 - 8)^2 = 4$.

Cross Entropy: Target = `[1, 0]`, Pred = `[0.9, 0.1]`.
Loss = $-(1 \\times \\log(0.9) + 0 \\times \\log(0.1)) \\approx 0.105$.

## 7. Code (Python, with type hints)
```python
import numpy as np

def mse_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean((y_true - y_pred) ** 2)

def binary_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    # Add epsilon to prevent log(0)
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
```

## 8. Common mistakes
- Using MSE for classification problems (it works poorly because the classification space isn't convex with MSE, leading to vanishing gradients).
- Forgetting to handle $\\log(0)$ in Cross-Entropy implementation, causing `NaN` errors.

## 9. 30-second interview answer
"A loss function measures the error between predictions and ground truth. Mean Squared Error (MSE) is standard for regression tasks, while Cross-Entropy is standard for classification. The goal of training is to minimize this function using gradient descent."

## 10. 2-minute interview answer
"Loss functions define the objective landscape for neural networks. For regression, we typically use L2 loss (MSE) which penalizes outliers quadratically, or L1 loss (MAE) for robustness to outliers. For classification, we use Cross-Entropy, which measures the information-theoretic distance between the predicted softmax probabilities and the true distribution. The critical requirement for any loss function is that it must be differentiable with respect to the network's outputs, because its derivative acts as the starting signal for Backpropagation. If the loss function is flat (zero gradient), the network cannot learn."

## 11. Follow-ups
- "Why use Cross-Entropy instead of MSE for Classification?" (Cross-entropy paired with Softmax provides well-scaled gradients, whereas MSE with Sigmoid/Softmax causes vanishing gradients when predictions are confidently wrong).

## 12. Deeper questions
- "What is Focal Loss?" (A modification of Cross-Entropy used in object detection that down-weights the loss assigned to easy-to-classify background examples, focusing on hard, minority class examples).

## 13. Related concepts
- **Gradients**: Calculated directly from the loss function.
- **Regularization**: Often added directly to the loss function (e.g., L2 penalty).

## 14. When it breaks / Edge cases
- Unscaled losses on massive batches can overflow float16/float32 limits.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Next-Token Prediction in LLMs uses Causal Language Modeling loss, which is just standard categorical Cross-Entropy applied to vocabulary probabilities.
"""

files["02-deep-learning/gradients.md"] = """# Gradients

## 1. Definition
A gradient is a vector containing the partial derivatives of a function with respect to all of its variables. In ML, it points in the direction of the steepest ascent of the Loss function.

## 2. Intuition
Imagine standing blindfolded on a hilly terrain, trying to find the lowest valley (min loss). You feel the slope of the ground under your feet. The gradient tells you which way is strictly "uphill". To reach the valley, you take a step in the *exact opposite* direction of the gradient.

## 3. Why it exists
Without gradients, we would have to guess randomly to update weights (Random Search). Gradients exist to provide mathematical, deterministic directions on exactly how to adjust every single weight to reduce the error.

## 4. Mechanics
If Loss $L = w^2$, the gradient with respect to $w$ is $\\frac{\\partial L}{\\partial w} = 2w$.
If $w = 3$, the gradient is 6. This means increasing $w$ slightly will increase $L$ sharply. So, we must *decrease* $w$.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(W)$ to compute for $W$ parameters.
- **Space Complexity:** $O(W)$ to store the gradient vector for the optimizer.

## 6. Tiny worked example
$L(w, b) = 3w + b^2$.
$\\frac{\\partial L}{\\partial w} = 3$.
$\\frac{\\partial L}{\\partial b} = 2b$.
The Gradient Vector $\\nabla L = [3, 2b]$.

## 7. Code (Python, with type hints)
```python
import torch

# PyTorch automates gradient calculation
w = torch.tensor([3.0], requires_grad=True)
b = torch.tensor([4.0], requires_grad=True)

loss = 3 * w + b ** 2
loss.backward()

print(w.grad) # tensor([3.])
print(b.grad) # tensor([8.])
```

## 8. Common mistakes
- Forgetting to zero out gradients (`optimizer.zero_grad()`) in PyTorch before the next batch, causing gradients to accumulate incorrectly.
- Vanishing/Exploding gradients in deep networks.

## 9. 30-second interview answer
"A gradient is a vector of partial derivatives representing the slope of the loss function with respect to the model's weights. Because the gradient points to the steepest increase in loss, we subtract it from the weights during gradient descent to minimize the error."

## 10. 2-minute interview answer
"The gradient is the compass that guides neural network training. Mathematically, it is the vector of partial derivatives of the loss function evaluated at the current weight values. It inherently points in the direction of steepest ascent in the high-dimensional loss landscape. Optimization algorithms like SGD calculate this gradient via backpropagation and then step in the negative direction, scaled by a learning rate, to descend into a loss minimum. The main challenges in deep learning—like vanishing or exploding gradients—occur when these partial derivatives multiply over many layers, collapsing to zero or shooting to infinity, effectively breaking the 'compass'."

## 11. Follow-ups
- "What causes vanishing gradients?" (Repeatedly multiplying derivatives $< 1$, commonly caused by deep networks using Sigmoid or Tanh activations).

## 12. Deeper questions
- "What is the Jacobian Matrix vs the Hessian Matrix?" (Jacobian is 1st-order partial derivatives for vector-valued functions. Hessian is 2nd-order derivatives, describing the curvature of the loss landscape).

## 13. Related concepts
- **Backpropagation**: The algorithm used to efficiently compute the gradients.
- **Gradient Descent**: The algorithm that uses the gradients to update weights.

## 14. When it breaks / Edge cases
- Non-differentiable functions (like step functions or `argmax`) have undefined or zero gradients, making gradient-based learning impossible.

## 15. Comparison with alternative approaches
- **vs Evolutionary Algorithms:** Evolutionary algorithms don't use gradients, making them immune to non-differentiable bottlenecks, but they are vastly less sample-efficient than gradient descent.

---
*Where this shows up in ML:* 
The `.grad` attribute of parameters in PyTorch.
"""

files["02-deep-learning/backpropagation.md"] = """# Backpropagation

## 1. Definition
Backpropagation is an algorithm that efficiently calculates the gradient of the loss function with respect to every weight in a neural network by applying the Chain Rule of calculus backwards from the output to the input.

## 2. Intuition
Imagine a factory line where the final product is defective. The manager (Loss) yells at the last worker. That worker says, "I assembled it wrong, but the guy before me gave me a bad part!" So they yell at the previous worker, passing the blame backward. Backprop calculates exactly how much "blame" (gradient) each weight deserves for the final error.

## 3. Why it exists
Calculating gradients naively by bumping each parameter slightly and doing a forward pass would take $O(W^2)$ time, which is impossible for networks with billions of parameters. Backprop uses dynamic programming (caching intermediates) to compute all gradients in a single backward pass, taking only $O(W)$ time.

## 4. Mechanics
1. Perform Forward Pass, caching intermediate activations.
2. Calculate the derivative of the Loss function at the output.
3. Multiply the derivative by the derivative of the activation function (Chain Rule).
4. Propagate this "error signal" backward through the weight matrices.
5. Store the resulting gradients for the optimizer to use.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(W)$, roughly 2x the computation of a forward pass.
- **Space Complexity:** $O(A)$ to store activations from the forward pass, which is the primary memory bottleneck in DL training.

## 6. Tiny worked example
Chain: $x \\xrightarrow{w_1} y \\xrightarrow{w_2} L$.
Let $L = y \\times w_2$, and $y = x \\times w_1$.
By Chain Rule: $\\frac{\\partial L}{\\partial w_1} = \\frac{\\partial L}{\\partial y} \\times \\frac{\\partial y}{\\partial w_1}$.
$\\frac{\\partial L}{\\partial y} = w_2$. $\\frac{\\partial y}{\\partial w_1} = x$.
Gradient for $w_1$ is $w_2 \\times x$.

## 7. Code (Python, with type hints)
```python
# Conceptual implementation of backward pass for Z = X * W
def linear_backward(dZ, X, W):
    # Gradient with respect to weights
    dW = X.T @ dZ
    # Gradient to pass further backward to previous layers
    dX = dZ @ W.T 
    return dX, dW
```

## 8. Common mistakes
- Confusing Backpropagation (calculating gradients) with Gradient Descent (updating weights).
- Forgetting that the chain rule is just matrix multiplication in deep learning.

## 9. 30-second interview answer
"Backpropagation is the algorithm used to compute gradients in a neural network. It applies the calculus chain rule recursively, passing error signals backward from the loss function to the input layer, allowing us to find the gradient of all parameters in $O(W)$ time."

## 10. 2-minute interview answer
"Backpropagation is essentially dynamic programming applied to calculus. To update weights, we need the derivative of the loss with respect to every parameter. Calculating this naively is computationally intractable. Instead, backprop utilizes the chain rule to recursively multiply local derivatives, starting from the output and moving backward. By caching the intermediate activations during the forward pass, backprop ensures that we only compute the shared derivatives once, achieving $O(W)$ time complexity. This efficiency is the single mathematical reason why training deep, parameter-dense neural networks is feasible on modern hardware."

## 11. Follow-ups
- "Why does backpropagation require so much memory?" (Because you must keep all intermediate activations in VRAM to compute the local derivatives during the backward pass).

## 12. Deeper questions
- "What is Gradient Accumulation?" (If a batch size doesn't fit in memory, you do forward/backward passes on micro-batches, adding the gradients together before performing a single optimizer step).

## 13. Related concepts
- **Chain Rule**: The mathematical theorem underlying Backprop.
- **Computational Graphs (Autograd)**: How modern frameworks implement Backprop.

## 14. When it breaks / Edge cases
- Breaks mathematically if activation functions are non-differentiable (like Heaviside step function).

## 15. Comparison with alternative approaches
- **vs Forward Mode Auto-Diff:** Forward mode computes derivatives while going forward. It's efficient when inputs are few and outputs are many. Backprop (Reverse mode) is efficient when inputs are many (millions of weights) and output is one (a single scalar Loss), which perfectly maps to ML.

---
*Where this shows up in ML:* 
Triggered via `loss.backward()` in PyTorch.
"""

files["02-deep-learning/gradient-descent.md"] = """# Gradient Descent

## 1. Definition
Gradient Descent is a first-order iterative optimization algorithm used to minimize a loss function by updating parameters in the opposite direction of the gradient.

## 2. Intuition
You are blindfolded on a mountain and want to reach the bottom. You feel the slope with your foot (calculate gradient), take a step downhill (update weights), and repeat until the ground feels flat (minimum loss).

## 3. Why it exists
For complex neural networks, there is no closed-form mathematical solution to find the minimum of the loss function (you can't just set the derivative to zero and solve for $W$). Gradient Descent exists to find the minimum numerically through iterative approximation.

## 4. Mechanics
1. Initialize weights randomly.
2. Compute the gradient of the loss $\\nabla L(W)$.
3. Update weights: $W_{new} = W_{old} - \\alpha \\nabla L(W)$, where $\\alpha$ is the Learning Rate.
4. Repeat until convergence.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(E \\times N \\times W)$ where $E$ is epochs, $N$ is samples, $W$ is parameters.
- **Space Complexity:** $O(W)$ to hold the gradients and weights.

## 6. Tiny worked example
Weight $w = 5$, Learning Rate $\\alpha = 0.1$.
Gradient is calculated as $2$.
Update: $w_{new} = 5 - (0.1 \\times 2) = 5 - 0.2 = 4.8$.

## 7. Code (Python, with type hints)
```python
import numpy as np

def gradient_descent_step(weights: np.ndarray, gradients: np.ndarray, lr: float) -> np.ndarray:
    return weights - lr * gradients
```

## 8. Common mistakes
- Setting the Learning Rate too high, causing the updates to overshoot the minimum and diverge (loss goes to infinity).
- Setting the Learning Rate too low, causing the model to take forever to train or get stuck in local minima.

## 9. 30-second interview answer
"Gradient descent is an optimization algorithm that minimizes the loss function. It iteratively subtracts the gradient of the loss from the weights, scaled by a learning rate, steering the model toward a local or global minimum."

## 10. 2-minute interview answer
"Gradient Descent is the workhorse of machine learning optimization. Since neural networks lack a closed-form solution, we must solve for the optimal weights iteratively. By calculating the gradient of the loss landscape via backpropagation, we know the direction of steepest ascent. Gradient descent simply steps in the exact opposite direction. The step size is controlled by the learning rate, which is the most critical hyperparameter: too high, and the model diverges; too low, and it stagnates. Standard 'Batch' Gradient Descent computes the gradient over the entire dataset before stepping, which provides a precise vector but is incredibly slow and memory-intensive, leading to the creation of Stochastic and Mini-Batch variants."

## 11. Follow-ups
- "What happens if you get stuck in a local minimum?" (In very high-dimensional spaces like Deep Learning, true local minima are rare; saddle points are the real issue. Momentum helps escape them).

## 12. Deeper questions
- "How do 2nd-order methods (like Newton's Method) differ?" (They compute the Hessian to know the curvature of the space, allowing massive, accurate steps, but computing a $W \\times W$ Hessian for 1B parameters is impossible).

## 13. Related concepts
- **Learning Rate**: Controls the step size.
- **SGD / Adam**: Advanced variants of basic Gradient Descent.

## 14. When it breaks / Edge cases
- Diverges to `NaN` if the learning rate is too large.

## 15. Comparison with alternative approaches
- **vs Closed Form (Normal Equation):** Linear regression can be solved exactly in one step taking $O(F^3)$ time (matrix inversion). Gradient descent is used when inversion is too slow or impossible (non-linear networks).

---
*Where this shows up in ML:* 
The underlying mechanism behind `optimizer.step()`.
"""

files["02-deep-learning/sgd.md"] = """# Stochastic Gradient Descent (SGD) & Mini-Batch SGD

## 1. Definition
Stochastic Gradient Descent (SGD) approximates the true gradient by evaluating the loss on a single random training example (or a small Mini-Batch) per step, rather than the entire dataset.

## 2. Intuition
Instead of surveying 10,000 people to perfectly decide which way to step (Batch GD), you ask 32 random people (Mini-Batch SGD). Their average opinion is a bit noisy, but it's "good enough" to take a step, and you can take hundreds of steps in the time it would take to survey all 10,000 once.

## 3. Why it exists
Standard Batch Gradient Descent requires evaluating the entire dataset to take *one* step. If you have 1 million images, it's computationally agonizing and doesn't fit in RAM. SGD allows frequent, lightweight updates, drastically accelerating training.

## 4. Mechanics
- **Pure SGD:** Batch size = 1. High noise, slow hardware utilization (no matrix parallelization).
- **Mini-Batch SGD:** Batch size = 16 to 1024. Strikes a balance: smooths out noise, fits in GPU memory, and perfectly utilizes GPU matrix parallelization.
- Often paired with **Momentum**: adding a fraction of the previous update to the current one to plow through noise and saddle points.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(B \\times W)$ per step, where $B$ is batch size.
- **Space Complexity:** $O(B \\times A)$ for activations. Fits nicely in GPU VRAM.

## 6. Tiny worked example
Dataset size 100.
- Batch GD: 1 step per epoch. True gradient.
- Mini-batch (size 10): 10 steps per epoch. Slightly noisy gradients.
- Pure SGD (size 1): 100 steps per epoch. Highly erratic gradients.

## 7. Code (Python, with type hints)
```python
import torch

# PyTorch Optimizer setup
# lr is learning rate, momentum helps smooth the SGD path
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Inside training loop:
# optimizer.zero_grad()
# loss.backward()
# optimizer.step()
```

## 8. Common mistakes
- Using pure SGD (batch size 1) in production. It completely wastes GPU parallelization capabilities.
- Not shuffling the dataset before creating mini-batches. If batches are ordered by class, the gradients will pull the model violently in different directions.

## 9. 30-second interview answer
"SGD optimizes neural networks by updating weights using a small mini-batch of data rather than the entire dataset. This introduces noise but allows for exponentially faster, more frequent updates and ensures the data fits into GPU memory."

## 10. 2-minute interview answer
"Mini-Batch SGD is the de facto standard for training neural networks. Computing the true gradient over millions of samples before taking a single step is computationally unfeasible. By sampling a random mini-batch—say, 256 images—we get an unbiased, slightly noisy estimate of the true gradient. This noise acts as a feature, not a bug, providing a regularizing effect that helps the model bounce out of shallow local minima. More importantly, it strikes the perfect balance for hardware: it fits within GPU VRAM constraints while being just large enough to max out SIMD matrix-multiplication efficiency. We almost always enhance it with Momentum, which acts like a moving average on the gradients, dampening the batch-to-batch oscillations and accelerating convergence along consistent dimensions."

## 11. Follow-ups
- "What happens if the batch size is too large?" (It mimics Batch GD: updates become rare, it requires massive memory, and ironically, generalizing performance often drops because the lack of noise causes it to settle into sharp local minima).

## 12. Deeper questions
- "How does Adam differ from SGD with Momentum?" (Adam uses adaptive learning rates for *each parameter* based on the 1st and 2nd moments of the gradients, whereas SGD applies the same learning rate to all parameters).

## 13. Related concepts
- **Adam Optimizer**: The most popular advanced alternative to SGD.
- **Batch Normalization**: Often needed to stabilize the erratic internal shifts caused by mini-batch updates.

## 14. When it breaks / Edge cases
- Breaks if the dataset isn't I.I.D (independent and identically distributed). Shuffling is mandatory.

## 15. Comparison with alternative approaches
- **vs Adam:** SGD with Momentum often generalizes slightly better on Computer Vision tasks (ResNets), while Adam converges much faster and is universally preferred for NLP/Transformers.

---
*Where this shows up in ML:* 
The core optimizer loop training every modern AI model.
"""

files["02-deep-learning/activation-functions.md"] = """# Activation Functions

## 1. Definition
Activation functions are mathematical equations applied to the output of a neural network node that determine whether and how strongly the neuron should "fire".

## 2. Intuition
If a network was a judicial system, the linear weights are lawyers presenting evidence (numbers). The activation function is the judge. The judge looks at the evidence and makes a non-linear ruling: "Guilty (1)", "Not Guilty (0)", or "Pay exactly this much (ReLU)".

## 3. Why it exists
Without activation functions, a neural network of 100 layers collapses mathematically into a single linear layer ($W_3(W_2(W_1x)) = W_{combined}x$). Activation functions inject **non-linearity**, allowing the network to learn complex, curved boundaries (like XOR or image features).

## 4. Mechanics
- **Sigmoid:** Squashes $(-\\infty, \\infty)$ to $(0, 1)$. Bad for hidden layers (vanishing gradients).
- **Tanh:** Squashes to $(-1, 1)$. Zero-centered, better than Sigmoid.
- **ReLU (Rectified Linear Unit):** $\\max(0, x)$. If negative, 0. If positive, passes through unchanged. Standard for hidden layers.
- **Softmax:** Converts a vector of scores into a probability distribution (summing to 1). Used in output layers for classification.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ element-wise operation.
- **Space Complexity:** $O(N)$ to cache the inputs for the backward pass.

## 6. Tiny worked example
Input $Z = [-2.0, 3.0]$.
ReLU(Z) = `[0.0, 3.0]`.
Sigmoid(Z) = `[0.11, 0.95]`.

## 7. Code (Python, with type hints)
```python
import numpy as np

def relu(z: np.ndarray) -> np.ndarray:
    return np.maximum(0, z)

def softmax(z: np.ndarray) -> np.ndarray:
    # Shift for numerical stability (prevent exp overflow)
    shifted_z = z - np.max(z)
    exps = np.exp(shifted_z)
    return exps / np.sum(exps)
```

## 8. Common mistakes
- Using Softmax in hidden layers (it destroys independent feature representations).
- Using Sigmoid in deep hidden layers, causing the "Vanishing Gradient Problem".

## 9. 30-second interview answer
"Activation functions introduce non-linearity into neural networks, allowing them to model complex, real-world data. ReLU is the standard for hidden layers because it avoids vanishing gradients. Softmax is used in output layers for multi-class probabilities."

## 10. 2-minute interview answer
"The primary purpose of activation functions is to break linearity. Without them, a deep network is mathematically equivalent to a single linear regression model. Historically, Sigmoid and Tanh were used, but they suffer from the Vanishing Gradient problem: for very high or low inputs, their derivative approaches zero, killing the backpropagation signal. ReLU solved this by providing a constant gradient of 1 for all positive inputs, allowing deep networks to actually train. However, ReLU can suffer from 'Dying ReLUs' where large negative bias updates permanently lock a neuron to 0. This led to variants like Leaky ReLU and modern NLP variants like GeLU. For the output layer, we almost universally use Softmax for classification, as it neatly normalizes raw logits into a valid probability distribution."

## 11. Follow-ups
- "What is the Dying ReLU problem?" (If a neuron's weights shift so that it only receives negative inputs, its gradient becomes 0, and it never updates again).

## 12. Deeper questions
- "Why is GeLU preferred in Transformers?" (Gaussian Error Linear Unit combines the properties of ReLU, Dropout, and Zoneout by weighting inputs by their value in a normal distribution, creating a smoother non-linearity).

## 13. Related concepts
- **Vanishing Gradients**: Directly caused by saturating activation functions.
- **Forward Propagation**: Where activations are applied.

## 14. When it breaks / Edge cases
- Exp() in Softmax overflows easily if logits are large; subtract the max logit before exponentiating (numerical stability).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Between every single linear/conv layer in a deep learning model.
"""

files["01-ml-basics/overfitting-underfitting.md"] = """# Overfitting and Underfitting

## 1. Definition
**Underfitting** occurs when a model is too simple to capture the underlying patterns in the data (high bias). **Overfitting** occurs when a model is too complex and memorizes the training noise instead of the signal (high variance).

## 2. Intuition
- **Underfitting:** A student who studies for a math test by only learning addition, failing to understand multiplication. They fail both the practice test and the real test.
- **Overfitting:** A student who memorizes the exact answers to the practice test questions without understanding the formulas. They score 100% on the practice test, but fail the real test.

## 3. Why it exists
The central goal of ML is **generalization**—performing well on unseen data. Overfitting/underfitting are the two failure modes of generalization, dictating the Bias-Variance Tradeoff.

## 4. Mechanics
- **Underfitting:** High Training Error, High Validation Error. Caused by insufficient model capacity (e.g., linear model for non-linear data) or excessive regularization.
- **Overfitting:** Low Training Error, High Validation Error. Caused by excessive model capacity (deep networks on small datasets), too many epochs, or lack of regularization.

## 5. Complexity (Time & Space)
- N/A - conceptual phenomenons.

## 6. Tiny worked example
Dataset: Housing prices (curves upward).
- Linear Regression (Underfit): Draws a straight line. Huge errors.
- 10th Degree Polynomial (Overfit): Wiggles wildly to perfectly touch every single training point. Predicts $0 for a house slightly outside the data.
- Quadratic (Just right): Captures the smooth upward curve.

## 7. Code (Python, with type hints)
```python
# Mitigating Overfitting with L2 Regularization (Weight Decay)
from sklearn.linear_model import Ridge

# alpha is the regularization strength. 
# High alpha pushes weights to 0 (fights overfitting, risks underfitting).
# Low alpha allows complex weights (risks overfitting).
model = Ridge(alpha=1.0) 
model.fit(X_train, y_train)
```

## 8. Common mistakes
- Continuing to train just because "training loss is still going down." You must monitor validation loss. If training goes down but validation goes up, you are overfitting.
- Evaluating the model on the test set repeatedly to tune hyperparameters (this overfits to the test set! You must use a separate validation set).

## 9. 30-second interview answer
"Underfitting means a model is too simple and fails to learn the data, showing high error on both training and validation sets. Overfitting means a model is too complex and memorizes noise, showing low training error but high validation error. We balance them using the Bias-Variance tradeoff."

## 10. 2-minute interview answer
"Overfitting and underfitting represent the fundamental tension in machine learning: the Bias-Variance tradeoff. Underfitting implies high bias; the model makes strong, incorrect assumptions and lacks the capacity to capture the data's complexity. We fix this by increasing model size, adding features, or training longer. Overfitting implies high variance; the model has so much capacity that it memorizes the idiosyncratic noise of the training set, destroying its ability to generalize to unseen data. We detect overfitting when training loss drops while validation loss spikes. To combat overfitting, we rely on regularization techniques: L1/L2 weight penalties, Dropout, Early Stopping, or simply gathering more training data to drown out the noise."

## 11. Follow-ups
- "What is Early Stopping?" (Monitoring validation loss during training and halting training the moment it begins to increase, preserving the model weights from before the overfitting started).
- "How does Dropout prevent overfitting?" (By randomly zeroing out neurons during training, it prevents the network from relying too heavily on any single feature, forcing redundant, robust representations).

## 12. Deeper questions
- "What is 'Double Descent' in modern Deep Learning?" (A phenomenon where, contrary to classical statistics, as model capacity increases past the point of overfitting, the test error drops again, suggesting massive models implicitly self-regularize).

## 13. Related concepts
- **Regularization**: The cure for overfitting.
- **Cross-Validation**: The method used to detect overfitting reliably.

## 14. When it breaks / Edge cases
- In NLP (LLMs), models are often trained for exactly 1 epoch over trillions of tokens. Traditional overfitting is rare because the model never sees the same data twice.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The core motivation behind architectural choices like Dropout layers in Vision, and Weight Decay in AdamW optimizers.
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch B - Sub-pass 1 Complete")
