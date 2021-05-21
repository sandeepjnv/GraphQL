import graphene
from graphene_django import DjangoObjectType
from .models import Books

class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields =("id","title","desc")

class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType)
    
    def resolve_all_books(root,info):
        return Books.objects.all() 

class NewBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        desc = graphene.String(required=True)

    book = graphene.Field(BooksType) 
    @classmethod
    def mutate(cls,root,info,title,desc):
        book = Books(title=title,desc=desc)
        book.save()
        return NewBook(book=book)    

class UpdateBook(graphene.Mutation):
    class Arguments:
        id =graphene.ID()
        title = graphene.String()
        desc = graphene.String()

    book = graphene.Field(BooksType)
    @classmethod
    def mutate(cls,root,info,id,title,desc):
        book = Books.objects.get(id=id)
        book.title=title
        book.desc=desc
        book.save()
        return UpdateBook(book=book) 

class Mutation(graphene.ObjectType):
    insertNewBook = NewBook.Field()
    updateBook = UpdateBook.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)