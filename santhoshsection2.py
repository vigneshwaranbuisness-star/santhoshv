import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_null_payment_object():
    from payment_gateway import validate_payment
    
    with pytest.raises(ValueError, match="[Pp]ayment.*[Nn]one|[Cc]annot be None|[Nn]ull"):
        validate_payment(None)


def test_log_parsing():
    log_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'logs',
        'error.log'
    )
    
    with open(log_path, 'r') as f:
        log_content = f.read()
    #
    assert "NoneType" in log_content
    assert "CRITICAL" in log_content
    assert "API_TIMEOUT" in log_content
    #

def test_stack_trace_line():
    trace_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'stack_trace.txt'
    )
    
    with open(trace_path, 'r') as f:
        trace_content = f.read()
    
  #
    assert "validate_payment" in trace_content
    assert "NoneType" in trace_content
#

def test_invalid_config():
    from payment_gateway import load_config
    
    config = load_config()
    
    assert isinstance(config['API_TIMEOUT'], int), \
        f"API_TIMEOUT should be int, got {type(config['API_TIMEOUT'])}"
    
    assert isinstance(config['MAX_RETRY'], int), \
        f"MAX_RETRY should be int, got {type(config['MAX_RETRY'])}"


def test_amount_validation():
    from payment_gateway import validate_payment
    
    negative_payment = {
        "amount": -100.00,
        "transaction_id": "TXN_NEG_001",
        "currency": "USD"
    }

    with pytest.raises(ValueError, match="[Aa]mount|[Nn]egative|[Pp]ositive"):
        validate_payment(negative_payment)


def test_transaction_rollback():
    from payment_gateway import execute_transaction
    
    bad_payment = {
        "amount": -500,
        "transaction_id": "TXN_ROLLBACK_001",
        "currency": "USD"
    }
    
    result = execute_transaction(bad_payment, 3)
    #
    assert result['status'] == "failed", "Failed transaction should have failed status"
    assert (
        'rollback' in result.get('reason', '').lower() or
        'rolled_back' in result or
        result.get('rolled_back', False) is True
    )
#

def test_error_handling():
    from payment_gateway import process_payment
    
    result = process_payment(None)
   # 
    assert result['status'] in ['error', 'failed']
    assert result['reason'] != "Processing failed"
    assert len(result['reason']) > 10
#

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
