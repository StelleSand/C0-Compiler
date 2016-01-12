int Fibonacci(int n)
{
    int a,b;
    a = Fibonacci(n - 1);
    b = Fibonacci(n - 2);
    return a+b ;
}
void main(int argv, int args)
{
    int n;
    scanf(n);
    printf(Fibonacci(n));
}