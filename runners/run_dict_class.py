from short_examples.DictClass import DictClass

d = dict(
    a=10,
    b=15,
    c=20
)

d_class = DictClass(d)
print(d)

# print("vars(d) = ", vars(d))
# print("dir(d) = ", dir(d))
# print("vars(d_class) = ", vars(d_class))
# print("dir(d_class) = ", dir(d_class))

print("d_class.a = ", d_class.a)
print("d_class.b = ", d_class.b)
print("d_class.c = ", d_class.c)
# print("d_class.d = ", d_class.d)
# print("d_class.e = ", d_class.e)

d["a"] = -1
print("d_class.a = ", d_class.a)
print("d_class.b = ", d_class.b)
print("d_class.c = ", d_class.c)
print("d_class.d = ", d_class.d)
