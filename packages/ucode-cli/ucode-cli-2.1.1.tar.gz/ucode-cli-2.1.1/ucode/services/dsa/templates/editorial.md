Vì $P$ rất lớn (đến $2^{31}-1$), nên ta cần thuật toán có độ phức tạp tính toán là $O(log(p))$ để tính $B^P$ và lấy $\mod M$ trong quá trình tính toán để tránh tràn số.

Thuật toán sử dụng công thức hồi quy như sau:

$$a^n = \begin{cases} 1 &\text{nếu } n = 0 \\ \left(a^{\frac{n}{2}}\right)^2 &\text{nếu } n > 0 \text{ và } n \text{ chẵn}\\ \left(a^{\frac{n - 1}{2}}\right)^2 \times a &\text{nếu } n > 0 \text{ và } n \text{ lẻ}\\ \end{cases}$$
        
