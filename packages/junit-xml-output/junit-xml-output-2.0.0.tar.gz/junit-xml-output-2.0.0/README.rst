*Create junit test xml output from python!*

Example Usage
~~~~~~~~~~~~~

.. code:: python

    import junit_xml_output
    test_cases = []
    test_cases.append(junit_xml_output.TestCase("first", "eg_contents",
        "failure"))
    junit_xml = junit_xml_output.JunitXml("example_usage", test_cases)
    print (junit_xml.dump())


