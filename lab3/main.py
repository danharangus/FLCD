from symbolTable import SymbolTable

if __name__ == "__main__":
    st = SymbolTable(2)
    st.insert(7)
    st.insert(5)
    st.insert("a")
    st.insert("variable")

    print(st.display())
    print(st.get("variable"))
    print(st.get("test"))
    print(st.get(10))

    st.display()