/*  Boolector: Satisfiability Modulo Theories (SMT) solver.
 *
 *  Copyright (C) 2018 Aina Niemetz.
 *
 *  This file is part of Boolector.
 *  See COPYING for more information on using this software.
 */

#include "pyboolector_abort.h"

#include <string>

class BoolectorException : public std::exception
{
 public:
  BoolectorException (const char* msg) : msg (msg) {}
    virtual ~BoolectorException() _GLIBCXX_USE_NOEXCEPT {}
  const char* what () const _GLIBCXX_USE_NOEXCEPT  { return msg.c_str(); }

 protected:
  std::string msg;
};

void pyboolector_abort_fun (const char* msg)
{
  throw BoolectorException (msg);
}

const char * pyboolector_get_err_msg ()
{
  try
  {
    throw;
  }
  catch (const BoolectorException& e)
  {
    return e.what ();
  }
}
