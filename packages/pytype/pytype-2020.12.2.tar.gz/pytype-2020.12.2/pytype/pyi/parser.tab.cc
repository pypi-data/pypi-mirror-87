// A Bison parser, made by GNU Bison 3.7.3.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015, 2018-2020 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
// especially those whose name start with YY_ or yy_.  They are
// private implementation details that can be changed or removed.


// Take the name prefix into account.
#define yylex   pytypelex



#include "parser.tab.hh"


// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 74 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif


// Whether we are compiled with exception support.
#ifndef YY_EXCEPTIONS
# if defined __GNUC__ && !defined __EXCEPTIONS
#  define YY_EXCEPTIONS 0
# else
#  define YY_EXCEPTIONS 1
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (false)
# endif


// Enable debugging if requested.
#if PYTYPEDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << '\n';                       \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yy_stack_print_ ();                \
  } while (false)

#else // !PYTYPEDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE (Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void> (0)
# define YY_STACK_PRINT()                static_cast<void> (0)

#endif // !PYTYPEDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
namespace pytype {
#line 167 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
#if PYTYPEDEBUG
    : yydebug_ (false),
      yycdebug_ (&std::cerr),
#else
    :
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}

  parser::syntax_error::~syntax_error () YY_NOEXCEPT YY_NOTHROW
  {}

  /*---------------.
  | symbol kinds.  |
  `---------------*/

  // basic_symbol.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& that)
    : Base (that)
    , value (that.value)
    , location (that.location)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_MOVE_REF (location_type) l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_RVREF (semantic_type) v, YY_RVREF (location_type) l)
    : Base (t)
    , value (YY_MOVE (v))
    , location (YY_MOVE (l))
  {}

  template <typename Base>
  parser::symbol_kind_type
  parser::basic_symbol<Base>::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }

  template <typename Base>
  bool
  parser::basic_symbol<Base>::empty () const YY_NOEXCEPT
  {
    return this->kind () == symbol_kind::S_YYEMPTY;
  }

  template <typename Base>
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move (s);
    value = YY_MOVE (s.value);
    location = YY_MOVE (s.location);
  }

  // by_kind.
  parser::by_kind::by_kind ()
    : kind_ (symbol_kind::S_YYEMPTY)
  {}

#if 201103L <= YY_CPLUSPLUS
  parser::by_kind::by_kind (by_kind&& that)
    : kind_ (that.kind_)
  {
    that.clear ();
  }
#endif

  parser::by_kind::by_kind (const by_kind& that)
    : kind_ (that.kind_)
  {}

  parser::by_kind::by_kind (token_kind_type t)
    : kind_ (yytranslate_ (t))
  {}

  void
  parser::by_kind::clear ()
  {
    kind_ = symbol_kind::S_YYEMPTY;
  }

  void
  parser::by_kind::move (by_kind& that)
  {
    kind_ = that.kind_;
    that.clear ();
  }

  parser::symbol_kind_type
  parser::by_kind::kind () const YY_NOEXCEPT
  {
    return kind_;
  }

  parser::symbol_kind_type
  parser::by_kind::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }


  // by_state.
  parser::by_state::by_state () YY_NOEXCEPT
    : state (empty_state)
  {}

  parser::by_state::by_state (const by_state& that) YY_NOEXCEPT
    : state (that.state)
  {}

  void
  parser::by_state::clear () YY_NOEXCEPT
  {
    state = empty_state;
  }

  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  parser::by_state::by_state (state_type s) YY_NOEXCEPT
    : state (s)
  {}

  parser::symbol_kind_type
  parser::by_state::kind () const YY_NOEXCEPT
  {
    if (state == empty_state)
      return symbol_kind::S_YYEMPTY;
    else
      return YY_CAST (symbol_kind_type, yystos_[+state]);
  }

  parser::stack_symbol_type::stack_symbol_type ()
  {}

  parser::stack_symbol_type::stack_symbol_type (YY_RVREF (stack_symbol_type) that)
    : super_type (YY_MOVE (that.state), YY_MOVE (that.value), YY_MOVE (that.location))
  {
#if 201103L <= YY_CPLUSPLUS
    // that is emptied.
    that.state = empty_state;
#endif
  }

  parser::stack_symbol_type::stack_symbol_type (state_type s, YY_MOVE_REF (symbol_type) that)
    : super_type (s, YY_MOVE (that.value), YY_MOVE (that.location))
  {
    // that is emptied.
    that.kind_ = symbol_kind::S_YYEMPTY;
  }

#if YY_CPLUSPLUS < 201103L
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (const stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    return *this;
  }

  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    // that is emptied.
    that.state = empty_state;
    return *this;
  }
#endif

  template <typename Base>
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.kind ())
    {
      case symbol_kind::S_NAME: // NAME
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 374 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_NUMBER: // NUMBER
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 380 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_STRING: // STRING
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 386 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_LEXERROR: // LEXERROR
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 392 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_start: // start
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 398 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_unit: // unit
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 404 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_alldefs: // alldefs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 410 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_classdef: // classdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 416 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_name: // class_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 422 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_parents: // parents
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_parent_list: // parent_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 434 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_parent: // parent
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 440 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_class_funcs: // maybe_class_funcs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 446 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_funcs: // class_funcs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 452 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_funcdefs: // funcdefs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 458 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_if_stmt: // if_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 464 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_if_and_elifs: // if_and_elifs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_if_stmt: // class_if_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 476 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_if_and_elifs: // class_if_and_elifs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 482 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_if_cond: // if_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 488 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_elif_cond: // elif_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 494 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_else_cond: // else_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 500 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_condition: // condition
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_version_tuple: // version_tuple
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 512 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_condition_op: // condition_op
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.str)); }
#line 518 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_constantdef: // constantdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_importdef: // importdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 530 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_import_items: // import_items
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 536 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_import_item: // import_item
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_import_name: // import_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 548 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_from_list: // from_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 554 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_from_items: // from_items
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 560 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_from_item: // from_item
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 566 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_alias_or_constant: // alias_or_constant
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 572 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_string_list: // maybe_string_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 578 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_string_list: // string_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 584 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevardef: // typevardef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 590 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevar_args: // typevar_args
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevar_kwargs: // typevar_kwargs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 602 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevar_kwarg: // typevar_kwarg
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 608 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_funcdef: // funcdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 614 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_funcname: // funcname
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 620 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_decorators: // decorators
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 626 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_decorator: // decorator
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 632 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_async: // maybe_async
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 638 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_params: // params
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 644 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_list: // param_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 650 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param: // param
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 656 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_type: // param_type
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 662 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_default: // param_default
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 668 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_star_name: // param_star_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 674 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_return: // return
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_body: // maybe_body
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 686 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_body: // body
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 692 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_body_stmt: // body_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 698 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_parameters: // type_parameters
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 704 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_parameter: // type_parameter
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 710 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_type_list: // maybe_type_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 716 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_list: // type_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 722 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type: // type
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 728 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_named_tuple_fields: // named_tuple_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 734 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_named_tuple_field_list: // named_tuple_field_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 740 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_named_tuple_field: // named_tuple_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 746 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_coll_named_tuple_fields: // coll_named_tuple_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 752 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_coll_named_tuple_field_list: // coll_named_tuple_field_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 758 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_coll_named_tuple_field: // coll_named_tuple_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typed_dict_fields: // typed_dict_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 770 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typed_dict_field_dict: // typed_dict_field_dict
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 776 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typed_dict_field: // typed_dict_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 782 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_typed_dict_kwarg: // maybe_typed_dict_kwarg
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 788 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_tuple_elements: // type_tuple_elements
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 794 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_tuple_literal: // type_tuple_literal
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 800 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_dotted_name: // dotted_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 806 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_getitem_key: // getitem_key
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 812 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_number: // maybe_number
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 818 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      default:
        break;
    }
  }

#if PYTYPEDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo, const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    if (yysym.empty ())
      yyo << "empty symbol";
    else
      {
        symbol_kind_type yykind = yysym.kind ();
        yyo << (yykind < YYNTOKENS ? "token" : "nterm")
            << ' ' << yysym.name () << " ("
            << yysym.location << ": ";
        YYUSE (yykind);
        yyo << ')';
      }
  }
#endif

  void
  parser::yypush_ (const char* m, YY_MOVE_REF (stack_symbol_type) sym)
  {
    if (m)
      YY_SYMBOL_PRINT (m, sym);
    yystack_.push (YY_MOVE (sym));
  }

  void
  parser::yypush_ (const char* m, state_type s, YY_MOVE_REF (symbol_type) sym)
  {
#if 201103L <= YY_CPLUSPLUS
    yypush_ (m, stack_symbol_type (s, std::move (sym)));
#else
    stack_symbol_type ss (s, sym);
    yypush_ (m, ss);
#endif
  }

  void
  parser::yypop_ (int n)
  {
    yystack_.pop (n);
  }

#if PYTYPEDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // PYTYPEDEBUG

  parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - YYNTOKENS] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - YYNTOKENS];
  }

  bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::operator() ()
  {
    return parse ();
  }

  int
  parser::parse ()
  {
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

#if YY_EXCEPTIONS
    try
#endif // YY_EXCEPTIONS
      {
    YYCDEBUG << "Starting parse\n";


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, YY_MOVE (yyla));

  /*-----------------------------------------------.
  | yynewstate -- push a new symbol on the stack.  |
  `-----------------------------------------------*/
  yynewstate:
    YYCDEBUG << "Entering state " << int (yystack_[0].state) << '\n';
    YY_STACK_PRINT ();

    // Accept?
    if (yystack_[0].state == yyfinal_)
      YYACCEPT;

    goto yybackup;


  /*-----------.
  | yybackup.  |
  `-----------*/
  yybackup:
    // Try to take a decision without lookahead.
    yyn = yypact_[+yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token\n";
#if YY_EXCEPTIONS
        try
#endif // YY_EXCEPTIONS
          {
            yyla.kind_ = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
#if YY_EXCEPTIONS
        catch (const syntax_error& yyexc)
          {
            YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
            error (yyexc);
            goto yyerrlab1;
          }
#endif // YY_EXCEPTIONS
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    if (yyla.kind () == symbol_kind::S_YYerror)
    {
      // The scanner already issued an error message, process directly
      // to error recovery.  But do not keep the error token as
      // lookahead, it is too special and may lead us to an endless
      // loop in error recovery. */
      yyla.kind_ = symbol_kind::S_YYUNDEF;
      goto yyerrlab1;
    }

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.kind ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.kind ())
      {
        goto yydefault;
      }

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", state_type (yyn), YY_MOVE (yyla));
    goto yynewstate;


  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[+yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;


  /*-----------------------------.
  | yyreduce -- do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_ (yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Default location.
      {
        stack_type::slice range (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, range, yylen);
        yyerror_range[1].location = yylhs.location;
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
#if YY_EXCEPTIONS
      try
#endif // YY_EXCEPTIONS
        {
          switch (yyn)
            {
  case 2: // start: unit "end of file"
#line 135 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1089 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 3: // start: TRIPLEQUOTED unit "end of file"
#line 136 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1095 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 4: // unit: alldefs
#line 140 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1101 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 5: // alldefs: alldefs constantdef
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1107 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 6: // alldefs: alldefs funcdef
#line 145 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1113 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 7: // alldefs: alldefs importdef
#line 146 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1119 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 8: // alldefs: alldefs alias_or_constant
#line 147 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1130 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 9: // alldefs: alldefs classdef
#line 153 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1136 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 10: // alldefs: alldefs typevardef
#line 154 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1142 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 11: // alldefs: alldefs if_stmt
#line 155 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1152 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 12: // alldefs: %empty
#line 160 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1158 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 15: // classdef: decorators CLASS class_name parents ':' maybe_type_ignore maybe_class_funcs
#line 173 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNNN)", (yystack_[6].value.obj), (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      // Fix location tracking. See funcdef.
      yylhs.location.begin = yystack_[4].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1169 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 16: // class_name: NAME
#line 182 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1182 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 17: // parents: '(' parent_list ')'
#line 193 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1188 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 18: // parents: '(' ')'
#line 194 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 1194 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 19: // parents: %empty
#line 195 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyList_New(0); }
#line 1200 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 20: // parent_list: parent_list ',' parent
#line 199 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1206 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 21: // parent_list: parent
#line 200 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1212 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 22: // parent: type
#line 204 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1218 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 23: // parent: NAME '=' type
#line 205 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1224 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 24: // parent: NAMEDTUPLE
#line 206 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyString_FromString("NamedTuple"); }
#line 1230 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 25: // parent: TYPEDDICT
#line 207 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", PyString_FromString("TypedDict"));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1239 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 26: // maybe_class_funcs: pass_or_ellipsis maybe_type_ignore
#line 214 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = PyList_New(0); }
#line 1245 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 27: // maybe_class_funcs: INDENT class_funcs DEDENT
#line 215 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1251 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 28: // maybe_class_funcs: INDENT TRIPLEQUOTED class_funcs DEDENT
#line 216 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1257 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 29: // class_funcs: pass_or_ellipsis
#line 220 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = PyList_New(0); }
#line 1263 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 30: // class_funcs: funcdefs
#line 221 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1269 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 31: // funcdefs: funcdefs constantdef
#line 225 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1275 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 32: // funcdefs: funcdefs alias_or_constant
#line 226 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1285 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 33: // funcdefs: funcdefs funcdef
#line 231 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1291 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 34: // funcdefs: funcdefs class_if_stmt
#line 232 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1301 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 35: // funcdefs: funcdefs classdef
#line 237 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1307 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 36: // funcdefs: %empty
#line 238 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1313 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 37: // if_stmt: if_and_elifs else_cond ':' INDENT alldefs DEDENT
#line 243 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1321 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 38: // if_stmt: if_and_elifs
#line 246 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1327 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 39: // if_and_elifs: if_cond ':' INDENT alldefs DEDENT
#line 251 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1335 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 40: // if_and_elifs: if_and_elifs elif_cond ':' INDENT alldefs DEDENT
#line 255 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1343 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 41: // class_if_stmt: class_if_and_elifs else_cond ':' INDENT funcdefs DEDENT
#line 268 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1351 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 42: // class_if_stmt: class_if_and_elifs
#line 271 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1357 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 43: // class_if_and_elifs: if_cond ':' INDENT funcdefs DEDENT
#line 276 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1365 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 44: // class_if_and_elifs: class_if_and_elifs elif_cond ':' INDENT funcdefs DEDENT
#line 280 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1373 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 45: // if_cond: IF condition
#line 292 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1379 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 46: // elif_cond: ELIF condition
#line 296 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1385 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 47: // else_cond: ELSE
#line 300 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1391 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 48: // condition: dotted_name condition_op STRING
#line 304 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1399 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 49: // condition: dotted_name condition_op version_tuple
#line 307 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1407 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 50: // condition: dotted_name '[' getitem_key ']' condition_op NUMBER
#line 310 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1415 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 51: // condition: dotted_name '[' getitem_key ']' condition_op version_tuple
#line 313 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                               {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1423 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 52: // condition: condition AND condition
#line 316 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1429 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 53: // condition: condition OR condition
#line 317 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1435 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 54: // condition: '(' condition ')'
#line 318 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1441 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 55: // version_tuple: '(' NUMBER ',' ')'
#line 322 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1447 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 56: // version_tuple: '(' NUMBER ',' NUMBER ')'
#line 323 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1453 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 57: // version_tuple: '(' NUMBER ',' NUMBER ',' NUMBER ')'
#line 324 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1461 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 58: // condition_op: '<'
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<"; }
#line 1467 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 59: // condition_op: '>'
#line 331 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">"; }
#line 1473 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 60: // condition_op: LE
#line 332 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<="; }
#line 1479 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 61: // condition_op: GE
#line 333 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">="; }
#line 1485 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 62: // condition_op: EQ
#line 334 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "=="; }
#line 1491 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 63: // condition_op: NE
#line 335 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "!="; }
#line 1497 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 64: // constantdef: NAME '=' NUMBER
#line 339 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 65: // constantdef: NAME '=' STRING
#line 343 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1515 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 66: // constantdef: NAME '=' type_tuple_literal
#line 347 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 67: // constantdef: NAME '=' ELLIPSIS
#line 351 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1533 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 68: // constantdef: NAME '=' ELLIPSIS TYPECOMMENT type maybe_type_ignore
#line 355 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                         {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 69: // constantdef: NAME ':' type maybe_type_ignore
#line 359 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1551 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 70: // constantdef: NAME ':' type '=' ELLIPSIS maybe_type_ignore
#line 363 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1560 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 71: // constantdef: TYPEDDICT ':' type maybe_type_ignore
#line 367 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", PyString_FromString("TypedDict"), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1569 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 72: // constantdef: TYPEDDICT ':' type '=' ELLIPSIS maybe_type_ignore
#line 371 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                      {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", PyString_FromString("TypedDict"), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1578 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 73: // importdef: IMPORT import_items maybe_type_ignore
#line 378 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                          {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1587 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 74: // importdef: FROM import_name IMPORT from_list maybe_type_ignore
#line 382 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 75: // importdef: FROM '.' IMPORT from_list maybe_type_ignore
#line 386 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1607 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 76: // importdef: FROM '.' '.' IMPORT from_list maybe_type_ignore
#line 392 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1618 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 77: // import_items: import_items ',' import_item
#line 401 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 78: // import_items: import_item
#line 402 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1630 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 79: // import_item: dotted_name
#line 406 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1636 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 80: // import_item: dotted_name AS NAME
#line 407 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1642 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 81: // import_name: dotted_name
#line 412 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1648 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 82: // import_name: '.' import_name
#line 413 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1657 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 83: // from_list: from_items
#line 420 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1663 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 84: // from_list: '(' from_items ')'
#line 421 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1669 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 85: // from_list: '(' from_items ',' ')'
#line 422 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1675 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 86: // from_items: from_items ',' from_item
#line 426 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                             { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1681 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 87: // from_items: from_item
#line 427 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1687 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 88: // from_item: NAME
#line 431 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1693 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 89: // from_item: NAMEDTUPLE
#line 432 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = PyString_FromString("NamedTuple");
    }
#line 1701 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 90: // from_item: COLL_NAMEDTUPLE
#line 435 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromString("namedtuple");
    }
#line 1709 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 91: // from_item: TYPEDDICT
#line 438 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              {
      (yylhs.value.obj) = PyString_FromString("TypedDict");
    }
#line 1717 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 92: // from_item: TYPEVAR
#line 441 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            {
      (yylhs.value.obj) = PyString_FromString("TypeVar");
    }
#line 1725 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 93: // from_item: '*'
#line 444 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        {
      (yylhs.value.obj) = PyString_FromString("*");
    }
#line 1733 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 94: // from_item: NAME AS NAME
#line 447 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1739 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 95: // alias_or_constant: NAME '=' type maybe_type_ignore
#line 451 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1745 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 96: // alias_or_constant: NAME '=' '[' maybe_string_list ']' maybe_type_ignore
#line 452 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                         { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[5].value.obj), (yystack_[2].value.obj)); }
#line 1751 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 97: // maybe_string_list: string_list maybe_comma
#line 456 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1757 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 98: // maybe_string_list: %empty
#line 457 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1763 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 99: // string_list: string_list ',' STRING
#line 461 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1769 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 100: // string_list: STRING
#line 462 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1775 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 101: // typevardef: NAME '=' TYPEVAR '(' STRING typevar_args ')'
#line 466 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1784 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 102: // typevar_args: %empty
#line 473 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1790 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 103: // typevar_args: ',' type_list
#line 474 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1796 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 104: // typevar_args: ',' typevar_kwargs
#line 475 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1802 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 105: // typevar_args: ',' type_list ',' typevar_kwargs
#line 476 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1808 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 106: // typevar_kwargs: typevar_kwargs ',' typevar_kwarg
#line 480 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1814 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 107: // typevar_kwargs: typevar_kwarg
#line 481 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 108: // typevar_kwarg: NAME '=' type
#line 485 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1826 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 109: // typevar_kwarg: NAME '=' STRING
#line 487 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1832 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 110: // funcdef: decorators maybe_async DEF funcname '(' maybe_type_ignore params ')' return maybe_body
#line 492 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NONNNN)", (yystack_[9].value.obj), (yystack_[8].value.obj), (yystack_[6].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      yylhs.location.begin = yystack_[7].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1847 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 111: // funcname: NAME
#line 505 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1853 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 112: // funcname: COLL_NAMEDTUPLE
#line 506 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = PyString_FromString("namedtuple"); }
#line 1859 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 113: // funcname: TYPEDDICT
#line 507 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = PyString_FromString("TypedDict"); }
#line 1865 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 114: // decorators: decorators decorator
#line 511 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1871 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 115: // decorators: %empty
#line 512 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1877 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 116: // decorator: '@' dotted_name maybe_type_ignore
#line 516 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1883 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 117: // maybe_async: ASYNC
#line 520 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = Py_True; }
#line 1889 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 118: // maybe_async: %empty
#line 521 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_False; }
#line 1895 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 119: // params: param_list maybe_comma
#line 525 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1901 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 120: // params: %empty
#line 526 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1907 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 121: // param_list: param_list ',' maybe_type_ignore param
#line 538 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1913 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 122: // param_list: param
#line 539 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1919 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 123: // param: NAME param_type param_default
#line 543 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1925 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 124: // param: '*'
#line 544 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1931 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 125: // param: param_star_name param_type
#line 545 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1937 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 126: // param: ELLIPSIS
#line 546 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1943 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 127: // param_type: ':' type
#line 550 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1949 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 128: // param_type: %empty
#line 551 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1955 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 129: // param_default: '=' NAME
#line 555 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1961 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 130: // param_default: '=' NUMBER
#line 556 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1967 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 131: // param_default: '=' ELLIPSIS
#line 557 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1973 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 132: // param_default: %empty
#line 558 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1979 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 133: // param_star_name: '*' NAME
#line 562 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1985 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 134: // param_star_name: '*' '*' NAME
#line 563 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1991 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 135: // return: ARROW type
#line 567 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1997 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 136: // return: %empty
#line 568 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2003 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 137: // typeignore: TYPECOMMENT NAME
#line 572 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { Py_DecRef((yystack_[0].value.obj)); }
#line 2009 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 138: // typeignore: TYPECOMMENT NAME '[' maybe_type_list ']'
#line 573 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                             {
      Py_DecRef((yystack_[3].value.obj));
      Py_DecRef((yystack_[1].value.obj));
    }
#line 2018 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 139: // maybe_body: ':' typeignore INDENT body DEDENT
#line 580 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2024 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 140: // maybe_body: ':' INDENT body DEDENT
#line 581 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2030 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 141: // maybe_body: empty_body
#line 582 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyList_New(0); }
#line 2036 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 149: // body: body body_stmt
#line 596 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 2042 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 150: // body: body_stmt
#line 597 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2048 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 151: // body_stmt: NAME '=' type
#line 601 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2054 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 152: // body_stmt: RAISE type
#line 602 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2060 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 153: // body_stmt: RAISE type '(' ')'
#line 603 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2066 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 154: // type_parameters: type_parameters ',' type_parameter
#line 607 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2072 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 155: // type_parameters: type_parameter
#line 608 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2078 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 156: // type_parameter: type
#line 612 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2084 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 157: // type_parameter: ELLIPSIS
#line 613 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 2090 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 158: // type_parameter: NUMBER
#line 615 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2096 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 159: // type_parameter: STRING
#line 616 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2102 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 160: // type_parameter: '[' maybe_type_list ']'
#line 618 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            {
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2111 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 161: // maybe_type_list: type_list maybe_comma
#line 625 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2117 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 162: // maybe_type_list: %empty
#line 626 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 2123 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 163: // type_list: type_list ',' type
#line 630 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2129 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 164: // type_list: type
#line 631 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2135 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 165: // type: dotted_name
#line 635 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2144 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 166: // type: dotted_name '[' '(' ')' ']'
#line 639 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), PyList_New(0));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2153 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 167: // type: dotted_name '[' type_parameters maybe_comma ']'
#line 643 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2162 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 168: // type: NAMEDTUPLE '(' STRING ',' named_tuple_fields maybe_comma ')'
#line 647 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                 {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2171 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 169: // type: COLL_NAMEDTUPLE '(' STRING ',' coll_named_tuple_fields maybe_comma ')'
#line 651 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                           {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2180 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 170: // type: TYPEDDICT '(' STRING ',' typed_dict_fields maybe_typed_dict_kwarg ')'
#line 655 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                          {
      (yylhs.value.obj) = ctx->Call(kNewTypedDict, "(NNN)", (yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2189 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 171: // type: '(' type ')'
#line 659 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2195 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 172: // type: type AND type
#line 660 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2201 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 173: // type: type OR type
#line 661 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2207 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 174: // type: '?'
#line 662 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2213 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 175: // type: NOTHING
#line 663 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2219 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 176: // named_tuple_fields: '[' named_tuple_field_list maybe_comma ']'
#line 667 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                               { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2225 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 177: // named_tuple_fields: '[' ']'
#line 668 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2231 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 178: // named_tuple_field_list: named_tuple_field_list ',' named_tuple_field
#line 672 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2237 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 179: // named_tuple_field_list: named_tuple_field
#line 673 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2243 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 180: // named_tuple_field: '(' STRING ',' type maybe_comma ')'
#line 677 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2249 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 183: // coll_named_tuple_fields: '[' coll_named_tuple_field_list maybe_comma ']'
#line 686 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2255 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 184: // coll_named_tuple_fields: '[' ']'
#line 687 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2261 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 185: // coll_named_tuple_field_list: coll_named_tuple_field_list ',' coll_named_tuple_field
#line 691 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                           {
      (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj));
    }
#line 2269 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 186: // coll_named_tuple_field_list: coll_named_tuple_field
#line 694 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2275 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 187: // coll_named_tuple_field: STRING
#line 698 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[0].value.obj), ctx->Value(kAnything)); }
#line 2281 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 188: // typed_dict_fields: '{' typed_dict_field_dict maybe_comma '}'
#line 702 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                              { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2287 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 189: // typed_dict_fields: '{' '}'
#line 703 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyDict_New(); }
#line 2293 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 190: // typed_dict_field_dict: typed_dict_field_dict ',' typed_dict_field
#line 707 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                               {
      PyDict_Update((yystack_[2].value.obj), (yystack_[0].value.obj));
      (yylhs.value.obj) = (yystack_[2].value.obj);
      Py_DECREF((yystack_[0].value.obj));
    }
#line 2303 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 191: // typed_dict_field_dict: typed_dict_field
#line 712 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2309 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 192: // typed_dict_field: STRING ':' NAME
#line 716 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = Py_BuildValue("{N: N}", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2315 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 193: // maybe_typed_dict_kwarg: ',' NAME '=' type maybe_comma
#line 720 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 2321 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 194: // maybe_typed_dict_kwarg: maybe_comma
#line 721 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_None; }
#line 2327 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 195: // type_tuple_elements: type_tuple_elements ',' type
#line 728 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2333 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 196: // type_tuple_elements: type ',' type
#line 729 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2339 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 197: // type_tuple_literal: '(' type_tuple_elements maybe_comma ')'
#line 738 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                            {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2348 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 198: // type_tuple_literal: '(' type ',' ')'
#line 743 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2357 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 199: // type_tuple_literal: type ','
#line 749 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2366 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 200: // dotted_name: NAME
#line 756 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2372 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 201: // dotted_name: dotted_name '.' NAME
#line 757 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2388 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 202: // getitem_key: NUMBER
#line 771 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2394 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 203: // getitem_key: maybe_number ':' maybe_number
#line 772 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2404 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 204: // getitem_key: maybe_number ':' maybe_number ':' maybe_number
#line 777 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                   {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2414 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 205: // maybe_number: NUMBER
#line 785 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2420 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 206: // maybe_number: %empty
#line 786 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = NULL; }
#line 2426 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;


#line 2430 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

            default:
              break;
            }
        }
#if YY_EXCEPTIONS
      catch (const syntax_error& yyexc)
        {
          YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
          error (yyexc);
          YYERROR;
        }
#endif // YY_EXCEPTIONS
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, YY_MOVE (yylhs));
    }
    goto yynewstate;


  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        context yyctx (*this, yyla);
        std::string msg = yysyntax_error_ (yyctx);
        error (yyla.location, YY_MOVE (msg));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.kind () == symbol_kind::S_YYEOF)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:
    /* Pacify compilers when the user code never invokes YYERROR and
       the label yyerrorlab therefore never appears in user code.  */
    if (false)
      YYERROR;

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    YY_STACK_PRINT ();
    goto yyerrlab1;


  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    // Pop stack until we find a state that shifts the error token.
    for (;;)
      {
        yyn = yypact_[+yystack_[0].state];
        if (!yy_pact_value_is_default_ (yyn))
          {
            yyn += symbol_kind::S_YYerror;
            if (0 <= yyn && yyn <= yylast_
                && yycheck_[yyn] == symbol_kind::S_YYerror)
              {
                yyn = yytable_[yyn];
                if (0 < yyn)
                  break;
              }
          }

        // Pop the current state because it cannot handle the error token.
        if (yystack_.size () == 1)
          YYABORT;

        yyerror_range[1].location = yystack_[0].location;
        yy_destroy_ ("Error: popping", yystack_[0]);
        yypop_ ();
        YY_STACK_PRINT ();
      }
    {
      stack_symbol_type error_token;

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = state_type (yyn);
      yypush_ ("Shifting", YY_MOVE (error_token));
    }
    goto yynewstate;


  /*-------------------------------------.
  | yyacceptlab -- YYACCEPT comes here.  |
  `-------------------------------------*/
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;


  /*-----------------------------------.
  | yyabortlab -- YYABORT comes here.  |
  `-----------------------------------*/
  yyabortlab:
    yyresult = 1;
    goto yyreturn;


  /*-----------------------------------------------------.
  | yyreturn -- parsing is finished, return the result.  |
  `-----------------------------------------------------*/
  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    YY_STACK_PRINT ();
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
#if YY_EXCEPTIONS
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack\n";
        // Do not try to display the values of the reclaimed symbols,
        // as their printers might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
#endif // YY_EXCEPTIONS
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what ());
  }

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr;
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              else
                goto append;

            append:
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }

  std::string
  parser::symbol_name (symbol_kind_type yysymbol)
  {
    return yytnamerr_ (yytname_[yysymbol]);
  }



  // parser::context.
  parser::context::context (const parser& yyparser, const symbol_type& yyla)
    : yyparser_ (yyparser)
    , yyla_ (yyla)
  {}

  int
  parser::context::expected_tokens (symbol_kind_type yyarg[], int yyargn) const
  {
    // Actual number of expected tokens
    int yycount = 0;

    int yyn = yypact_[+yyparser_.yystack_[0].state];
    if (!yy_pact_value_is_default_ (yyn))
      {
        /* Start YYX at -YYN if negative to avoid negative indexes in
           YYCHECK.  In other words, skip the first -YYN actions for
           this state because they are default actions.  */
        int yyxbegin = yyn < 0 ? -yyn : 0;
        // Stay within bounds of both yycheck and yytname.
        int yychecklim = yylast_ - yyn + 1;
        int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
        for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
          if (yycheck_[yyx + yyn] == yyx && yyx != symbol_kind::S_YYerror
              && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
            {
              if (!yyarg)
                ++yycount;
              else if (yycount == yyargn)
                return 0;
              else
                yyarg[yycount++] = YY_CAST (symbol_kind_type, yyx);
            }
      }

    if (yyarg && yycount == 0 && 0 < yyargn)
      yyarg[0] = symbol_kind::S_YYEMPTY;
    return yycount;
  }



  int
  parser::yy_syntax_error_arguments_ (const context& yyctx,
                                                 symbol_kind_type yyarg[], int yyargn) const
  {
    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state merging
         (from LALR or IELR) and default reductions corrupt the expected
         token list.  However, the list is correct for canonical LR with
         one exception: it will still contain any token that will not be
         accepted due to an error action in a later state.
    */

    if (!yyctx.lookahead ().empty ())
      {
        if (yyarg)
          yyarg[0] = yyctx.token ();
        int yyn = yyctx.expected_tokens (yyarg ? yyarg + 1 : yyarg, yyargn - 1);
        return yyn + 1;
      }
    return 0;
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (const context& yyctx) const
  {
    // Its maximum.
    enum { YYARGS_MAX = 5 };
    // Arguments of yyformat.
    symbol_kind_type yyarg[YYARGS_MAX];
    int yycount = yy_syntax_error_arguments_ (yyctx, yyarg, YYARGS_MAX);

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
      default: // Avoid compiler warnings.
        YYCASE_ (0, YY_("syntax error"));
        YYCASE_ (1, YY_("syntax error, unexpected %s"));
        YYCASE_ (2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_ (3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_ (4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_ (5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    std::ptrdiff_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += symbol_name (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short parser::yypact_ninf_ = -359;

  const short parser::yytable_ninf_ = -206;

  const short
  parser::yypact_[] =
  {
      53,  -359,    41,   122,   364,   130,  -359,  -359,   -13,    18,
     155,    34,   132,  -359,  -359,   341,   163,  -359,  -359,  -359,
    -359,  -359,    68,  -359,   265,    25,  -359,    18,   168,   385,
     162,  -359,   134,    22,   149,   146,   265,  -359,    18,   182,
     184,   241,  -359,   212,   155,  -359,   223,  -359,   258,   290,
     299,   265,  -359,   150,    54,  -359,  -359,   323,   266,   265,
     370,   291,  -359,   358,    18,    18,  -359,  -359,  -359,  -359,
     271,  -359,  -359,   387,   104,   395,   155,  -359,  -359,   401,
     310,    64,  -359,   310,   349,   168,   334,   351,  -359,  -359,
     350,   116,   148,   417,   421,   430,   360,   265,   265,   380,
    -359,   133,   433,   265,   301,   402,  -359,   398,   403,  -359,
    -359,  -359,   428,  -359,   408,   404,   409,  -359,  -359,   442,
    -359,   407,  -359,  -359,   431,  -359,  -359,  -359,  -359,   102,
    -359,   414,   412,  -359,   310,    49,   414,   425,  -359,  -359,
    -359,   217,   165,   418,  -359,  -359,  -359,  -359,   416,   419,
     420,   422,  -359,   440,  -359,   414,  -359,  -359,  -359,   201,
     265,   423,  -359,   297,   424,    99,   233,   265,   426,   414,
     450,  -359,   389,   452,   427,   265,   456,   383,  -359,   102,
     414,  -359,   414,   227,   337,  -359,   429,   258,   299,  -359,
     386,  -359,   297,   414,   414,   432,   434,   435,  -359,   436,
     437,   438,   297,   171,   439,   270,   444,  -359,  -359,   297,
     297,  -359,  -359,  -359,    28,  -359,   447,    55,   443,  -359,
    -359,   321,  -359,  -359,  -359,  -359,  -359,   265,  -359,   300,
     232,     8,   238,   441,    79,   441,    14,   448,  -359,  -359,
     265,  -359,  -359,  -359,   446,   449,  -359,   451,  -359,  -359,
    -359,   452,   396,  -359,  -359,  -359,   297,  -359,  -359,  -359,
     376,  -359,   414,   453,  -359,    11,   454,   455,  -359,   453,
     459,  -359,   457,  -359,  -359,   460,  -359,  -359,   458,  -359,
     461,   464,  -359,   462,  -359,   463,  -359,   465,   297,   261,
     466,   270,  -359,  -359,   467,   220,   469,   239,  -359,  -359,
     265,   468,  -359,   470,   445,   362,  -359,  -359,   471,   472,
     473,  -359,   485,   474,  -359,   489,   498,   475,   477,  -359,
    -359,   297,   446,  -359,   449,   476,   478,  -359,   260,  -359,
    -359,   341,   482,  -359,  -359,  -359,   297,   375,  -359,  -359,
     265,   483,     8,   265,  -359,  -359,  -359,  -359,  -359,  -359,
    -359,   265,  -359,  -359,   205,   484,   486,   480,  -359,  -359,
    -359,   297,   377,  -359,  -359,  -359,   264,   264,   481,   491,
    -359,   180,   379,   414,   488,  -359,  -359,  -359,   286,   487,
     265,   495,    87,  -359,   496,   374,  -359,  -359,  -359,   325,
     338,  -359,   265,   371,  -359,  -359,  -359,  -359,   125,   497,
    -359,  -359,   297,   493,  -359,  -359,  -359
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   115,     0,     1,     2,     0,     0,
       0,     0,     0,     9,    11,    38,     0,     5,     7,     8,
      10,     6,   118,     3,     0,     0,   200,     0,    45,     0,
      14,    78,    79,     0,     0,    81,     0,    47,     0,     0,
       0,     0,   117,     0,     0,   114,     0,   175,     0,     0,
       0,     0,   174,    14,   165,    64,    65,     0,    67,     0,
      98,    14,    66,     0,     0,     0,    62,    63,    60,    61,
     206,    58,    59,     0,     0,     0,     0,    73,    13,     0,
       0,     0,    82,     0,    14,    46,     0,     0,    12,    16,
      19,    14,     0,     0,     0,     0,     0,     0,     0,     0,
      69,     0,     0,     0,     0,   182,   100,     0,   182,   199,
      95,    54,    53,    52,   202,     0,     0,   201,    48,     0,
      49,   137,    77,    80,    88,    89,    90,    91,    92,     0,
      93,    14,    83,    87,     0,     0,    14,     0,    71,    12,
      12,   115,     0,     0,   116,   111,   112,   113,     0,     0,
       0,     0,   171,   173,   172,    14,   158,   159,   157,     0,
     162,   182,   155,   156,   102,    14,     0,   181,     0,    14,
     181,    97,     0,   206,     0,   162,     0,     0,    75,     0,
      14,    74,    14,   115,   115,    39,   200,    24,    25,    18,
       0,    21,    22,    14,    14,     0,     0,     0,    70,     0,
       0,   182,   164,   181,     0,     0,     0,    68,   198,   196,
     195,   197,    96,    99,     0,   205,   203,     0,     0,    94,
      84,     0,    86,    76,    72,    40,    37,     0,    17,     0,
       0,   120,     0,   182,     0,   182,     0,   182,   166,   160,
     181,   161,   154,   167,   200,   104,   107,   103,   101,    50,
      51,   206,     0,    55,   138,    85,    23,    20,   207,   208,
      36,    15,    14,   128,   126,   124,     0,   182,   122,   128,
       0,   177,   182,   179,   181,     0,   187,   184,   182,   186,
       0,     0,   189,   182,   191,   181,   194,     0,   163,     0,
       0,     0,   204,    56,     0,    36,     0,   115,    29,    26,
       0,   132,   133,     0,   136,    14,   119,   125,     0,   181,
       0,   168,   181,     0,   169,     0,   181,     0,     0,   170,
     109,   108,     0,   106,   105,     0,     0,    27,     0,    35,
      34,    42,     0,    31,    32,    33,   127,     0,   123,   134,
       0,   148,     0,     0,   178,   176,   185,   183,   192,   190,
     188,     0,    57,    28,     0,     0,     0,     0,   129,   130,
     131,   135,     0,   110,   141,   121,   182,   182,     0,     0,
      36,     0,     0,   142,     0,   193,    36,    36,   115,     0,
       0,     0,     0,   150,     0,     0,   144,   143,   180,   115,
     115,    43,     0,   152,   147,   140,   149,   146,     0,     0,
      44,    41,   151,     0,   139,   145,   153
  };

  const short
  parser::yypgoto_[] =
  {
    -359,  -359,   503,   -82,   -48,  -293,  -359,  -359,  -359,   246,
    -359,   172,    60,  -359,  -359,  -359,  -359,  -289,   174,   175,
       4,   280,   348,  -287,  -359,  -359,   479,   512,   -74,   405,
    -159,  -279,  -359,  -359,  -359,  -359,   240,   242,  -274,  -359,
    -359,  -359,  -359,  -359,  -359,   191,   267,  -359,  -359,  -359,
     -66,  -359,  -359,   152,  -358,  -359,   332,   363,   335,   -24,
    -359,  -359,   230,  -106,  -359,  -359,   229,  -359,  -359,   226,
    -359,  -359,  -359,     6,  -359,  -170,  -223
  };

  const short
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    77,    13,    90,   143,   190,   191,
     261,   296,   297,    14,    15,   330,   331,    16,    39,    40,
      28,   120,    74,    17,    18,    30,    31,    82,   131,   132,
     133,    19,   107,   108,    20,   206,   245,   246,    21,   148,
      22,    45,    46,   266,   267,   268,   301,   338,   269,   341,
      78,   363,   364,   382,   383,   161,   162,   200,   201,   202,
     233,   272,   273,   168,   235,   278,   279,   237,   283,   284,
     287,   105,    62,    54,   115,   116,   298
  };

  const short
  parser::yytable_[] =
  {
      53,    61,   171,   216,   329,   100,   141,   262,   332,   136,
     333,   263,    84,   110,   302,    29,    32,    35,   334,   281,
     222,    26,    24,   335,   396,    26,    25,    96,    26,    55,
      56,    63,   249,    29,   264,   104,   138,    26,    80,    35,
     396,     6,    85,   144,    29,    47,    48,    49,    50,    57,
      91,    58,    26,   265,    27,   204,   303,   183,   184,   252,
     180,    59,   222,   282,   119,    60,    81,    26,   112,   113,
      29,    29,    52,   153,   154,    42,    43,   163,    33,   165,
     134,   292,    32,   178,   276,   329,     1,    35,   181,   332,
     379,   333,   253,   135,   101,   241,   329,   329,    73,   334,
     332,   332,   333,   333,   335,   124,   380,   198,   135,   118,
     334,   334,    97,    98,    44,   335,   335,   207,   192,   395,
     277,   212,     7,   125,   126,   127,   128,   275,   379,   280,
      23,   286,   223,    75,   224,    96,    26,   156,   157,   373,
     119,    35,   209,   210,   380,   230,   231,   130,   384,   386,
      75,   145,    79,    47,    48,    49,    50,   404,    26,   158,
      73,   306,   399,    97,    98,    83,   310,    36,   186,   159,
     146,   147,   313,   160,    26,   156,   157,   317,    73,   163,
      52,    64,    65,   379,    75,    47,   187,    49,   188,    99,
      73,    47,    48,    49,    50,   258,    75,   158,    41,   380,
      76,    51,   189,   256,    26,   192,   259,    51,    26,    55,
      56,   160,    52,   381,   299,    89,   288,    86,    52,    87,
       8,    47,    48,    49,    50,    47,    48,    49,    50,     9,
       8,    58,    92,    10,    11,   258,    26,    51,   199,     9,
      12,    59,   328,    10,    11,    60,   259,   258,    52,   185,
      12,     9,    52,    47,    48,    49,    50,   342,   259,   225,
     374,   375,    12,   260,    26,   321,   320,   288,    26,    51,
     208,   -30,    88,   244,   270,   114,   336,    97,    98,   271,
      52,    47,    48,    49,    50,    47,    48,    49,    50,   328,
      47,    48,    49,    50,    93,    24,   372,    51,     9,   354,
     103,    51,   274,   186,    97,    98,    51,   387,    52,    12,
      97,    98,    52,   124,    97,    98,   361,    52,   391,   366,
      47,   187,    49,   188,   124,    75,    94,   367,   328,   109,
      61,   125,   126,   127,   128,    95,    51,     9,   152,   166,
       8,   328,   125,   126,   127,   128,   129,    52,    12,     9,
       9,    37,    38,    10,    11,   130,   393,   400,   255,   102,
      12,    12,    97,    98,    -4,   139,   130,     8,   402,   226,
     401,    64,    65,    97,    98,   106,     9,   379,   358,   359,
      10,    11,   140,    75,    97,    98,   142,    12,   137,   258,
     117,   258,   258,   380,   258,   111,    75,   152,   121,  -181,
     259,   360,   259,   259,   123,   259,   155,   403,   371,   295,
     385,    75,    66,    67,    68,    69,    66,    67,    68,    69,
     220,   221,   149,   228,   229,    70,   150,    71,    72,    73,
     378,    71,    72,   293,   294,   151,   389,   390,   164,   169,
     167,   170,    65,  -205,   173,   172,   174,   175,    75,   176,
     179,   182,   194,   193,    98,   213,   215,   195,   196,   219,
     197,   203,   205,   211,   308,   217,   318,   326,   227,   322,
     340,   325,   232,   339,   234,   257,   240,   238,   239,   274,
     243,   248,   251,   236,   254,   289,   285,   290,   300,   291,
     276,   304,   348,   305,   250,   309,   312,   311,   314,   315,
     316,   327,   319,   281,     5,   355,   356,   337,   270,   343,
     353,   370,   376,   352,   345,   347,   351,   357,   362,   368,
     214,   369,   377,    34,   350,   388,   392,   394,   397,   405,
     406,   324,   323,   365,   177,   242,   307,   398,   218,   344,
     247,   346,   349,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,   122
  };

  const short
  parser::yycheck_[] =
  {
      24,    25,   108,   173,   297,    53,    88,   230,   297,    83,
     297,     3,    36,    61,     3,     9,    10,    11,   297,     5,
     179,     3,    35,   297,   382,     3,    39,    51,     3,     4,
       5,    27,     4,    27,    26,    59,    84,     3,    16,    33,
     398,     0,    38,    91,    38,    20,    21,    22,    23,    24,
      44,    26,     3,    45,    36,   161,    45,   139,   140,     4,
     134,    36,   221,    49,    36,    40,    44,     3,    64,    65,
      64,    65,    47,    97,    98,     7,     8,   101,    44,   103,
      16,   251,    76,   131,     5,   378,    33,    81,   136,   378,
       3,   378,    37,    44,    40,   201,   389,   390,    44,   378,
     389,   390,   389,   390,   378,     3,    19,   155,    44,     5,
     389,   390,    13,    14,    46,   389,   390,   165,   142,    32,
      41,   169,     0,    21,    22,    23,    24,   233,     3,   235,
       0,   237,   180,    34,   182,   159,     3,     4,     5,   362,
      36,   135,   166,   167,    19,   193,   194,    45,   371,   372,
      34,     3,    18,    20,    21,    22,    23,    32,     3,    26,
      44,   267,   385,    13,    14,    16,   272,    35,     3,    36,
      22,    23,   278,    40,     3,     4,     5,   283,    44,   203,
      47,    13,    14,     3,    34,    20,    21,    22,    23,    39,
      44,    20,    21,    22,    23,    15,    34,    26,    35,    19,
      38,    36,    37,   227,     3,   229,    26,    36,     3,     4,
       5,    40,    47,    33,   262,     3,   240,    35,    47,    35,
       3,    20,    21,    22,    23,    20,    21,    22,    23,    12,
       3,    26,     9,    16,    17,    15,     3,    36,    37,    12,
      23,    36,     3,    16,    17,    40,    26,    15,    47,    32,
      23,    12,    47,    20,    21,    22,    23,   305,    26,    32,
     366,   367,    23,    31,     3,   289,     5,   291,     3,    36,
      37,    32,    31,     3,    36,     4,   300,    13,    14,    41,
      47,    20,    21,    22,    23,    20,    21,    22,    23,     3,
      20,    21,    22,    23,    36,    35,   362,    36,    12,    39,
      34,    36,    38,     3,    13,    14,    36,   373,    47,    23,
      13,    14,    47,     3,    13,    14,   340,    47,    32,   343,
      20,    21,    22,    23,     3,    34,    36,   351,     3,    38,
     354,    21,    22,    23,    24,    36,    36,    12,    37,    38,
       3,     3,    21,    22,    23,    24,    36,    47,    23,    12,
      12,    10,    11,    16,    17,    45,   380,    32,    37,    36,
      23,    23,    13,    14,     0,    31,    45,     3,   392,    32,
      32,    13,    14,    13,    14,     5,    12,     3,     3,     4,
      16,    17,    31,    34,    13,    14,    36,    23,    39,    15,
       3,    15,    15,    19,    15,    37,    34,    37,     3,    37,
      26,    26,    26,    26,     3,    26,    26,    36,    31,    33,
      31,    34,    27,    28,    29,    30,    27,    28,    29,    30,
      37,    38,     5,    37,    38,    40,     5,    42,    43,    44,
     370,    42,    43,    37,    38,     5,   376,   377,     5,    41,
      38,    38,    14,    35,    35,    41,     4,    40,    34,    18,
      38,    26,    36,    35,    14,     5,     4,    38,    38,     3,
      38,    38,    38,    37,     5,    38,     3,   295,    39,     3,
      25,     4,    40,     3,    40,   229,    38,    41,    41,    38,
      41,    37,    35,    48,    41,    39,    38,    38,    35,    38,
       5,    37,     3,    38,   214,    38,    38,    37,    37,    35,
      38,    32,    37,     5,     1,   331,   331,    39,    36,    38,
      32,    31,    31,    37,    41,    41,    39,    35,    35,    35,
     172,    35,    31,    11,    49,    37,    39,    32,    32,    32,
      37,   291,   290,   342,   129,   203,   269,   385,   175,   309,
     205,   312,   316,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    76
  };

  const signed char
  parser::yystos_[] =
  {
       0,    33,    51,    52,    53,    52,     0,     0,     3,    12,
      16,    17,    23,    55,    63,    64,    67,    73,    74,    81,
      84,    88,    90,     0,    35,    39,     3,    36,    70,   123,
      75,    76,   123,    44,    77,   123,    35,    10,    11,    68,
      69,    35,     7,     8,    46,    91,    92,    20,    21,    22,
      23,    36,    47,   109,   123,     4,     5,    24,    26,    36,
      40,   109,   122,    70,    13,    14,    27,    28,    29,    30,
      40,    42,    43,    44,    72,    34,    38,    54,   100,    18,
      16,    44,    77,    16,   109,    70,    35,    35,    31,     3,
      56,   123,     9,    36,    36,    36,   109,    13,    14,    39,
      54,    40,    36,    34,   109,   121,     5,    82,    83,    38,
      54,    37,    70,    70,     4,   124,   125,     3,     5,    36,
      71,     3,    76,     3,     3,    21,    22,    23,    24,    36,
      45,    78,    79,    80,    16,    44,    78,    39,    54,    31,
      31,    53,    36,    57,    54,     3,    22,    23,    89,     5,
       5,     5,    37,   109,   109,    26,     4,     5,    26,    36,
      40,   105,   106,   109,     5,   109,    38,    38,   113,    41,
      38,   113,    41,    35,     4,    40,    18,    79,    54,    38,
      78,    54,    26,    53,    53,    32,     3,    21,    23,    37,
      58,    59,   109,    35,    36,    38,    38,    38,    54,    37,
     107,   108,   109,    38,   113,    38,    85,    54,    37,   109,
     109,    37,    54,     5,    72,     4,   125,    38,   107,     3,
      37,    38,    80,    54,    54,    32,    32,    39,    37,    38,
      54,    54,    40,   110,    40,   114,    48,   117,    41,    41,
      38,   113,   106,    41,     3,    86,    87,   108,    37,     4,
      71,    35,     4,    37,    41,    37,   109,    59,    15,    26,
      31,    60,   126,     3,    26,    45,    93,    94,    95,    98,
      36,    41,   111,   112,    38,   113,     5,    41,   115,   116,
     113,     5,    49,   118,   119,    38,   113,   120,   109,    39,
      38,    38,   125,    37,    38,    33,    61,    62,   126,    54,
      35,    96,     3,    45,    37,    38,   113,    96,     5,    38,
     113,    37,    38,   113,    37,    35,    38,   113,     3,    37,
       5,   109,     3,    87,    86,     4,    61,    32,     3,    55,
      65,    66,    67,    73,    81,    88,   109,    39,    97,     3,
      25,    99,    54,    38,   112,    41,   116,    41,     3,   119,
      49,    39,    37,    32,    39,    68,    69,    35,     3,     4,
      26,   109,    35,   101,   102,    95,   109,   109,    35,    35,
      31,    31,   100,   126,   113,   113,    31,    31,    62,     3,
      19,    33,   103,   104,   126,    31,   126,   100,    37,    62,
      62,    32,    39,   109,    32,    32,   104,    32,   103,   126,
      32,    32,   109,    36,    32,    32,    37
  };

  const signed char
  parser::yyr1_[] =
  {
       0,    50,    51,    51,    52,    53,    53,    53,    53,    53,
      53,    53,    53,    54,    54,    55,    56,    57,    57,    57,
      58,    58,    59,    59,    59,    59,    60,    60,    60,    61,
      61,    62,    62,    62,    62,    62,    62,    63,    63,    64,
      64,    65,    65,    66,    66,    67,    68,    69,    70,    70,
      70,    70,    70,    70,    70,    71,    71,    71,    72,    72,
      72,    72,    72,    72,    73,    73,    73,    73,    73,    73,
      73,    73,    73,    74,    74,    74,    74,    75,    75,    76,
      76,    77,    77,    78,    78,    78,    79,    79,    80,    80,
      80,    80,    80,    80,    80,    81,    81,    82,    82,    83,
      83,    84,    85,    85,    85,    85,    86,    86,    87,    87,
      88,    89,    89,    89,    90,    90,    91,    92,    92,    93,
      93,    94,    94,    95,    95,    95,    95,    96,    96,    97,
      97,    97,    97,    98,    98,    99,    99,   100,   100,   101,
     101,   101,   102,   102,   102,   102,   102,   102,   102,   103,
     103,   104,   104,   104,   105,   105,   106,   106,   106,   106,
     106,   107,   107,   108,   108,   109,   109,   109,   109,   109,
     109,   109,   109,   109,   109,   109,   110,   110,   111,   111,
     112,   113,   113,   114,   114,   115,   115,   116,   117,   117,
     118,   118,   119,   120,   120,   121,   121,   122,   122,   122,
     123,   123,   124,   124,   124,   125,   125,   126,   126
  };

  const signed char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     7,     1,     3,     2,     0,
       3,     1,     1,     3,     1,     1,     2,     3,     4,     1,
       1,     2,     2,     2,     2,     2,     0,     6,     1,     5,
       6,     6,     1,     5,     6,     2,     2,     1,     3,     3,
       6,     6,     3,     3,     3,     4,     5,     7,     1,     1,
       1,     1,     1,     1,     3,     3,     3,     3,     6,     4,
       6,     4,     6,     3,     5,     5,     6,     3,     1,     1,
       3,     1,     2,     1,     3,     4,     3,     1,     1,     1,
       1,     1,     1,     1,     3,     4,     6,     2,     0,     3,
       1,     7,     0,     2,     2,     4,     3,     1,     3,     3,
      10,     1,     1,     1,     2,     0,     3,     1,     0,     2,
       0,     4,     1,     3,     1,     2,     1,     2,     0,     2,
       2,     2,     0,     2,     3,     2,     0,     2,     5,     5,
       4,     1,     2,     3,     3,     5,     4,     4,     0,     2,
       1,     3,     2,     4,     3,     1,     1,     1,     1,     1,
       3,     2,     0,     3,     1,     1,     5,     5,     7,     7,
       7,     3,     3,     3,     1,     1,     4,     2,     3,     1,
       6,     1,     0,     4,     2,     3,     1,     1,     4,     2,
       3,     1,     3,     5,     1,     3,     3,     4,     4,     2,
       1,     3,     1,     3,     5,     1,     0,     1,     1
  };


#if PYTYPEDEBUG || 1
  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a YYNTOKENS, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "\"invalid token\"", "NAME", "NUMBER",
  "STRING", "LEXERROR", "ASYNC", "CLASS", "DEF", "ELSE", "ELIF", "IF",
  "OR", "AND", "PASS", "IMPORT", "FROM", "AS", "RAISE", "NOTHING",
  "NAMEDTUPLE", "COLL_NAMEDTUPLE", "TYPEDDICT", "TYPEVAR", "ARROW",
  "ELLIPSIS", "EQ", "NE", "LE", "GE", "INDENT", "DEDENT", "TRIPLEQUOTED",
  "TYPECOMMENT", "':'", "'('", "')'", "','", "'='", "'['", "']'", "'<'",
  "'>'", "'.'", "'*'", "'@'", "'?'", "'{'", "'}'", "$accept", "start",
  "unit", "alldefs", "maybe_type_ignore", "classdef", "class_name",
  "parents", "parent_list", "parent", "maybe_class_funcs", "class_funcs",
  "funcdefs", "if_stmt", "if_and_elifs", "class_if_stmt",
  "class_if_and_elifs", "if_cond", "elif_cond", "else_cond", "condition",
  "version_tuple", "condition_op", "constantdef", "importdef",
  "import_items", "import_item", "import_name", "from_list", "from_items",
  "from_item", "alias_or_constant", "maybe_string_list", "string_list",
  "typevardef", "typevar_args", "typevar_kwargs", "typevar_kwarg",
  "funcdef", "funcname", "decorators", "decorator", "maybe_async",
  "params", "param_list", "param", "param_type", "param_default",
  "param_star_name", "return", "typeignore", "maybe_body", "empty_body",
  "body", "body_stmt", "type_parameters", "type_parameter",
  "maybe_type_list", "type_list", "type", "named_tuple_fields",
  "named_tuple_field_list", "named_tuple_field", "maybe_comma",
  "coll_named_tuple_fields", "coll_named_tuple_field_list",
  "coll_named_tuple_field", "typed_dict_fields", "typed_dict_field_dict",
  "typed_dict_field", "maybe_typed_dict_kwarg", "type_tuple_elements",
  "type_tuple_literal", "dotted_name", "getitem_key", "maybe_number",
  "pass_or_ellipsis", YY_NULLPTR
  };
#endif


#if PYTYPEDEBUG
  const short
  parser::yyrline_[] =
  {
       0,   135,   135,   136,   140,   144,   145,   146,   147,   153,
     154,   155,   160,   164,   165,   172,   182,   193,   194,   195,
     199,   200,   204,   205,   206,   207,   214,   215,   216,   220,
     221,   225,   226,   231,   232,   237,   238,   243,   246,   251,
     255,   268,   271,   276,   280,   292,   296,   300,   304,   307,
     310,   313,   316,   317,   318,   322,   323,   324,   330,   331,
     332,   333,   334,   335,   339,   343,   347,   351,   355,   359,
     363,   367,   371,   378,   382,   386,   392,   401,   402,   406,
     407,   412,   413,   420,   421,   422,   426,   427,   431,   432,
     435,   438,   441,   444,   447,   451,   452,   456,   457,   461,
     462,   466,   473,   474,   475,   476,   480,   481,   485,   487,
     491,   505,   506,   507,   511,   512,   516,   520,   521,   525,
     526,   538,   539,   543,   544,   545,   546,   550,   551,   555,
     556,   557,   558,   562,   563,   567,   568,   572,   573,   580,
     581,   582,   586,   587,   588,   589,   590,   591,   592,   596,
     597,   601,   602,   603,   607,   608,   612,   613,   615,   616,
     618,   625,   626,   630,   631,   635,   639,   643,   647,   651,
     655,   659,   660,   661,   662,   663,   667,   668,   672,   673,
     677,   681,   682,   686,   687,   691,   694,   698,   702,   703,
     707,   712,   716,   720,   721,   728,   729,   738,   743,   749,
     756,   757,   771,   772,   777,   785,   786,   790,   791
  };

  void
  parser::yy_stack_print_ () const
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << int (i->state);
    *yycdebug_ << '\n';
  }

  void
  parser::yy_reduce_print_ (int yyrule) const
  {
    int yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):\n";
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // PYTYPEDEBUG

  parser::symbol_kind_type
  parser::yytranslate_ (int t)
  {
    // YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to
    // TOKEN-NUM as returned by yylex.
    static
    const signed char
    translate_table[] =
    {
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      36,    37,    45,     2,    38,     2,    44,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    35,     2,
      42,    39,    43,    47,    46,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    40,     2,    41,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    48,     2,    49,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34
    };
    // Last valid token kind.
    const int code_max = 289;

    if (t <= 0)
      return symbol_kind::S_YYEOF;
    else if (t <= code_max)
      return YY_CAST (symbol_kind_type, translate_table[t]);
    else
      return symbol_kind::S_YYUNDEF;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
} // pytype
#line 3264 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

#line 794 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
