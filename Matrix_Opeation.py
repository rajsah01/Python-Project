import numpy as np

def get_matrix(name):
    rows = int(input(f"\nEnter number of rows for Matrix {name}: "))
    cols = int(input(f"Enter number of columns for Matrix {name}: "))
    print(f"Enter elements of Matrix {name} row-wise (space-separated):")
    elements = []

    for i in range(rows):
        row = list(map(float, input(f"Row {i+1}: ").split()))
        if len(row) != cols:
            raise ValueError("Incorrect number of columns entered.")
        elements.append(row)

    return np.array(elements)

def matrix_addition(A, B):
    return A + B

def matrix_subtraction(A, B):
    return A - B

def matrix_multiplication(A, B):
    return A @ B

def matrix_transpose(A):
    return A.T

def matrix_determinant(A):
    if A.shape[0] != A.shape[1]:
        raise ValueError("Determinant can only be calculated for square matrices.")
    return np.linalg.det(A)

def display_menu():
    print("\n========== Matrix Operations Tool ==========")
    print("1. Add Matrices")
    print("2. Subtract Matrices")
    print("3. Multiply Matrices")
    print("4. Transpose Matrix")
    print("5. Determinant of Matrix")
    print("6. Exit")
    print("============================================")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")

        try:
            if choice == '1':
                A = get_matrix("A")
                B = get_matrix("B")
                if A.shape != B.shape:
                    print("❌ Error: Matrices must have the same dimensions.")
                    continue
                print("\n✅ Result of A + B:\n", matrix_addition(A, B))

            elif choice == '2':
                A = get_matrix("A")
                B = get_matrix("B")
                if A.shape != B.shape:
                    print("❌ Error: Matrices must have the same dimensions.")
                    continue
                print("\n✅ Result of A - B:\n", matrix_subtraction(A, B))

            elif choice == '3':
                A = get_matrix("A")
                B = get_matrix("B")
                if A.shape[1] != B.shape[0]:
                    print("❌ Error: Incompatible dimensions for multiplication.")
                    continue
                print("\n✅ Result of A * B:\n", matrix_multiplication(A, B))

            elif choice == '4':
                A = get_matrix("A")
                print("\n✅ Transpose of Matrix A:\n", matrix_transpose(A))

            elif choice == '5':
                A = get_matrix("A")
                det = matrix_determinant(A)
                print(f"\n✅ Determinant of Matrix A: {det:.2f}")

            elif choice == '6':
                print("\n👋 Exiting Matrix Operations Tool. Goodbye!")
                break

            else:
                print("❌ Invalid choice. Please enter a number from 1 to 6.")

        except Exception as e:
            print(f"⚠ Error: {e}")

if __name__ == "__main__":
    main()
