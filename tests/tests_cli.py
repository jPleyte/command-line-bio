import subprocess

def test_gff_transcript_query_help():
    """
    Test that the specific GFF transcript tool is installed.
    """
    # Note the updated command name here:
    result = subprocess.run(['clb-gff-t', '--help'], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()