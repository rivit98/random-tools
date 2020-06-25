#include <random>
#include <iostream>
#include <algorithm>
#include <stack>
#include <chrono>

int partition(std::vector<int> &arr, int low, int high) {
	int pivot = arr[high];
	int i = (low - 1);
	for (int j = low; j <= high - 1; j++) {
		if (arr[j] <= pivot) {
			i++;
			std::swap(arr[i], arr[j]);
		}
	}
	std::swap(arr[i + 1], arr[high]);
	return (i + 1);
}

void quickSortIterative(std::vector<int> &arr) {
	std::stack<std::pair<int, int>> callStack;
	callStack.push({0, arr.size() - 1});

	while(!callStack.empty()){
		auto [low, high] = callStack.top();
		callStack.pop();

		if(low < high){
			int pi = partition(arr, low, high);
			callStack.push({pi + 1, high});
			callStack.push({low, pi - 1});
		}
	}
}

void printVector(const std::vector<int> &numbers_vec) {
	for (auto &val : numbers_vec) {
		std::cout << val << " ";
	}
	std::cout << std::endl;
}

int main() {
//	std::random_device rd;
//	std::mt19937 gen{rd()};
	auto seed = std::chrono::system_clock::now().time_since_epoch().count();
	std::mt19937 gen(seed);

	std::uniform_int_distribution<> arraySizeUniform(1, 20);
	std::uniform_int_distribution<> valuesUniform(-15, 15);
	int aSize = arraySizeUniform(gen);

	std::vector<int> orig(aSize);
	std::transform(orig.begin(), orig.end(), orig.begin(),
				   [&gen, &valuesUniform](auto &v) {
					   return valuesUniform(gen);
				   });

	printVector(orig);
	std::vector<int> iterative(orig);
	std::sort(orig.begin(), orig.end());
	quickSortIterative(iterative);

	std::cout << "Sorted original values: ";
	printVector(orig);

	std::cout << "Sorted iterative values: ";
	printVector(iterative);

	std::cout << std::boolalpha;

	std::cout << "Correct? " << (orig == iterative) << "\n";
//	std::cout << "Correct? " << std::equal(orig.begin(), orig.end(), iterative.begin()) << "\n";


	return 0;
}